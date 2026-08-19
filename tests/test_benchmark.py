from pathlib import Path

from src.benchmark import BenchmarkSettings, run_benchmark, write_outputs


def test_tiny_cpu_benchmark_writes_expected_files(tmp_path: Path) -> None:
    settings = BenchmarkSettings(
        sequence_lengths=(8,),
        models=("rnn",),
        batch_size=2,
        vocab_size=100,
        hidden_size=16,
        num_layers=1,
        transformer_heads=4,
        warmup=0,
        repeats=1,
        device="cpu",
    )
    rows = run_benchmark(settings)
    assert len(rows) == 1
    assert rows[0]["status"] == "ok"
    assert float(rows[0]["latency_ms_mean"]) > 0

    write_outputs(rows, settings, tmp_path)
    assert (tmp_path / "benchmark.csv").is_file()
    assert (tmp_path / "run_config.json").is_file()
    assert (tmp_path / "tradeoff_summary.md").is_file()

