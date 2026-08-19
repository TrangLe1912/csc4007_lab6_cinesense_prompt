"""CLI entry point for CSC4007 Lab 6."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.benchmark import BenchmarkSettings, run_benchmark, write_outputs


SUPPORTED_MODELS = ("rnn", "lstm", "gru", "transformer", "mamba")


def comma_separated_ints(value: str) -> tuple[int, ...]:
    try:
        parsed = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("sequence lengths must be comma-separated integers") from exc
    if not parsed or any(item < 1 for item in parsed):
        raise argparse.ArgumentTypeError("sequence lengths must be positive")
    return parsed


def comma_separated_models(value: str) -> tuple[str, ...]:
    parsed = tuple(item.strip().lower() for item in value.split(",") if item.strip())
    invalid = sorted(set(parsed) - set(SUPPORTED_MODELS))
    if not parsed or invalid:
        raise argparse.ArgumentTypeError(f"unsupported model(s): {', '.join(invalid)}")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark long-sequence backbones for CSC4007 Lab 6")
    parser.add_argument("--sequence-lengths", type=comma_separated_ints, default=(128, 256, 512, 1024))
    parser.add_argument("--models", type=comma_separated_models, default=SUPPORTED_MODELS)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--vocab-size", type=int, default=20_000)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=1)
    parser.add_argument("--transformer-heads", type=int, default=4)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--seed", type=int, default=4007)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument(
        "--include-mamba",
        choices=("auto", "yes", "no"),
        default="auto",
        help="yes adds Mamba, no removes it, auto follows --models",
    )
    parser.add_argument("--smoke", action="store_true", help="run a tiny, fast configuration")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    models = list(args.models)
    if args.include_mamba == "yes" and "mamba" not in models:
        models.append("mamba")
    if args.include_mamba == "no":
        models = [name for name in models if name != "mamba"]
    if not models:
        raise SystemExit("No models selected")

    sequence_lengths = args.sequence_lengths
    warmup = args.warmup
    repeats = args.repeats
    batch_size = args.batch_size
    if args.smoke:
        sequence_lengths = (8, 16)
        warmup = 0
        repeats = 1
        batch_size = min(batch_size, 2)

    settings = BenchmarkSettings(
        sequence_lengths=tuple(sequence_lengths),
        models=tuple(models),
        batch_size=batch_size,
        vocab_size=args.vocab_size,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        transformer_heads=args.transformer_heads,
        warmup=warmup,
        repeats=repeats,
        seed=args.seed,
        device=args.device,
    )
    rows = run_benchmark(settings)
    write_outputs(rows, settings, args.output_dir)

    print(f"Wrote {len(rows)} rows to {args.output_dir / 'benchmark.csv'}")
    for row in rows:
        print(
            f"{row['model']:>11} seq={row['sequence_length']:<5} "
            f"status={row['status']:<13} latency_ms={row['latency_ms_mean']}"
        )


if __name__ == "__main__":
    main()

