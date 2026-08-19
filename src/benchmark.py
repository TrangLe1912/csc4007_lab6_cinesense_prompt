"""Reproducible forward-pass benchmark utilities for Lab 6."""

from __future__ import annotations

import csv
import json
import math
import os
import platform
import resource
import statistics
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import psutil
import torch

from .models import ModelConfig, OptionalDependencyError, build_model, count_parameters


CSV_FIELDS = [
    "model",
    "sequence_length",
    "batch_size",
    "hidden_size",
    "num_layers",
    "device",
    "status",
    "latency_ms_mean",
    "latency_ms_std",
    "throughput_tokens_per_s",
    "peak_memory_mb",
    "memory_method",
    "parameters",
    "notes",
]


@dataclass(frozen=True)
class BenchmarkSettings:
    sequence_lengths: tuple[int, ...] = (128, 256, 512, 1024)
    models: tuple[str, ...] = ("rnn", "lstm", "gru", "transformer", "mamba")
    batch_size: int = 8
    vocab_size: int = 20_000
    hidden_size: int = 64
    num_layers: int = 1
    transformer_heads: int = 4
    warmup: int = 3
    repeats: int = 10
    seed: int = 4007
    device: str = "auto"
    memory_sample_interval_s: float = 0.002


class RssSampler:
    """Best-effort CPU RSS delta sampler; not a tensor-allocation profiler."""

    def __init__(self, interval_s: float) -> None:
        self.interval_s = interval_s
        try:
            self.process: psutil.Process | None = psutil.Process(os.getpid())
            self.method = "sampled_rss_delta"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Some teaching sandboxes expose a transient host PID.  The
            # standard-library high-water RSS value is a safe fallback.
            self.process = None
            self.method = "resource_peak_rss_delta"
        self.baseline = self._current_rss()
        self.peak = self.baseline
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._sample, daemon=True)

    def _current_rss(self) -> int:
        if self.process is not None:
            try:
                return self.process.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.process = None
                self.method = "resource_peak_rss_delta"
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Linux reports KiB; macOS reports bytes.
        return int(value if platform.system() == "Darwin" else value * 1024)

    def _sample(self) -> None:
        while not self._stop.is_set():
            self.peak = max(self.peak, self._current_rss())
            self._stop.wait(self.interval_s)

    def __enter__(self) -> "RssSampler":
        self._thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.peak = max(self.peak, self._current_rss())
        self._stop.set()
        self._thread.join(timeout=1.0)

    @property
    def delta_mb(self) -> float:
        return max(0.0, self.peak - self.baseline) / (1024**2)


def resolve_device(requested: str) -> torch.device:
    if requested == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is False")
    return torch.device(requested)


def _synchronize(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def _empty_row(
    model_name: str,
    sequence_length: int,
    settings: BenchmarkSettings,
    device: torch.device,
    status: str,
    notes: str,
) -> dict[str, object]:
    return {
        "model": model_name,
        "sequence_length": sequence_length,
        "batch_size": settings.batch_size,
        "hidden_size": settings.hidden_size,
        "num_layers": settings.num_layers,
        "device": str(device),
        "status": status,
        "latency_ms_mean": "",
        "latency_ms_std": "",
        "throughput_tokens_per_s": "",
        "peak_memory_mb": "",
        "memory_method": "not_measured",
        "parameters": "",
        "notes": notes,
    }


def run_benchmark(settings: BenchmarkSettings) -> list[dict[str, object]]:
    if settings.warmup < 0 or settings.repeats < 1:
        raise ValueError("warmup must be >= 0 and repeats must be >= 1")
    if any(length < 1 for length in settings.sequence_lengths):
        raise ValueError("all sequence lengths must be positive")

    torch.manual_seed(settings.seed)
    device = resolve_device(settings.device)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(settings.seed)

    config = ModelConfig(
        vocab_size=settings.vocab_size,
        hidden_size=settings.hidden_size,
        num_layers=settings.num_layers,
        transformer_heads=settings.transformer_heads,
    )
    rows: list[dict[str, object]] = []

    for model_name in settings.models:
        try:
            model = build_model(model_name, config).to(device).eval()
            parameters = count_parameters(model)
        except OptionalDependencyError as exc:
            rows.extend(
                _empty_row(
                    model_name,
                    length,
                    settings,
                    device,
                    "not_installed",
                    str(exc),
                )
                for length in settings.sequence_lengths
            )
            continue
        except Exception as exc:  # preserve build failures as evidence
            rows.extend(
                _empty_row(
                    model_name,
                    length,
                    settings,
                    device,
                    "build_error",
                    f"{type(exc).__name__}: {exc}",
                )
                for length in settings.sequence_lengths
            )
            continue

        for sequence_length in settings.sequence_lengths:
            token_ids = torch.randint(
                0,
                settings.vocab_size,
                (settings.batch_size, sequence_length),
                device=device,
            )
            latencies_ms: list[float] = []
            peak_memory_mb = 0.0
            memory_method = "cuda_peak_allocated" if device.type == "cuda" else "sampled_rss_delta"

            try:
                with torch.inference_mode():
                    for _ in range(settings.warmup):
                        _ = model(token_ids)
                    _synchronize(device)

                    if device.type == "cuda":
                        torch.cuda.reset_peak_memory_stats(device)
                        for _ in range(settings.repeats):
                            _synchronize(device)
                            started = time.perf_counter()
                            _ = model(token_ids)
                            _synchronize(device)
                            latencies_ms.append((time.perf_counter() - started) * 1000)
                        peak_memory_mb = torch.cuda.max_memory_allocated(device) / (1024**2)
                    else:
                        with RssSampler(settings.memory_sample_interval_s) as sampler:
                            for _ in range(settings.repeats):
                                started = time.perf_counter()
                                _ = model(token_ids)
                                latencies_ms.append((time.perf_counter() - started) * 1000)
                        peak_memory_mb = sampler.delta_mb
                        memory_method = sampler.method

                mean_ms = statistics.fmean(latencies_ms)
                std_ms = statistics.pstdev(latencies_ms) if len(latencies_ms) > 1 else 0.0
                throughput = settings.batch_size * sequence_length / (mean_ms / 1000)
                rows.append(
                    {
                        "model": model_name,
                        "sequence_length": sequence_length,
                        "batch_size": settings.batch_size,
                        "hidden_size": settings.hidden_size,
                        "num_layers": settings.num_layers,
                        "device": str(device),
                        "status": "ok",
                        "latency_ms_mean": round(mean_ms, 4),
                        "latency_ms_std": round(std_ms, 4),
                        "throughput_tokens_per_s": round(throughput, 2),
                        "peak_memory_mb": round(peak_memory_mb, 4),
                        "memory_method": memory_method,
                        "parameters": parameters,
                        "notes": "",
                    }
                )
            except RuntimeError as exc:
                status = "oom" if "out of memory" in str(exc).lower() else "runtime_error"
                row = _empty_row(model_name, sequence_length, settings, device, status, str(exc))
                row["parameters"] = parameters
                rows.append(row)
                if device.type == "cuda":
                    torch.cuda.empty_cache()

        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    return rows


def environment_info(settings: BenchmarkSettings) -> dict[str, object]:
    return {
        "settings": asdict(settings),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "cpu_logical_count": psutil.cpu_count(logical=True),
    }


def write_outputs(
    rows: Iterable[dict[str, object]],
    settings: BenchmarkSettings,
    output_dir: str | Path,
) -> None:
    materialized = list(rows)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    with (destination / "benchmark.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(materialized)

    (destination / "run_config.json").write_text(
        json.dumps(environment_info(settings), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (destination / "tradeoff_summary.md").write_text(
        render_markdown_summary(materialized),
        encoding="utf-8",
    )


def _fmt(value: object) -> str:
    if value == "" or value is None:
        return "—"
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return "—"
    return str(value)


def render_markdown_summary(rows: Iterable[dict[str, object]]) -> str:
    lines = [
        "# Trade-off summary",
        "",
        "> Đây là benchmark compute trên token tổng hợp, không phải metric chất lượng NLP.",
        "",
        "| Model | Seq. length | Status | Latency mean (ms) | Throughput (token/s) | Peak memory (MB) | Params |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {model} | {sequence_length} | {status} | {latency_ms_mean} | "
            "{throughput_tokens_per_s} | {peak_memory_mb} | {parameters} |".format(
                **{key: _fmt(value) for key, value in row.items()}
            )
        )
    lines.extend(
        [
            "",
            "## Câu hỏi phân tích",
            "",
            "1. Xu hướng latency và memory theo độ dài chuỗi khác nhau thế nào?",
            "2. Số tham số và backend/device ảnh hưởng tính công bằng ra sao?",
            "3. Kết quả nào là bằng chứng chất lượng tác vụ, kết quả nào chỉ là chi phí compute?",
            "4. Bạn chọn mô hình nào cho bối cảnh cụ thể và giới hạn của kết luận là gì?",
            "",
        ]
    )
    return "\n".join(lines)
