# Extracted from C:/!ass-ade/scripts/lora_training/train_lora.py:171
# Component id: sy.source.ass_ade.main
from __future__ import annotations

__version__ = "0.1.0"

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--data",
        type=Path,
        default=Path("training_data/training_data.jsonl"),
        help="Path to training_data.jsonl.",
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("models/lora_adapter"),
        help="Where to save the adapter (default: models/lora_adapter/).",
    )
    ap.add_argument("--base", default=_DEFAULT_BASE, help="Base model HF id.")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lora-rank", type=int, default=8)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--min-samples", type=int, default=10)
    args = ap.parse_args()

    if not args.data.exists():
        print(f"[train] ERROR: {args.data} not found. Run collect_training_data.py first.", file=sys.stderr)
        sys.exit(1)

    adapter_dir = train(
        data_path=args.data.resolve(),
        output_dir=args.output_dir.resolve(),
        base_model=args.base,
        epochs=args.epochs,
        lora_rank=args.lora_rank,
        batch_size=args.batch_size,
        max_length=args.max_length,
        min_samples=args.min_samples,
    )
    print(f"[train] done — adapter at {adapter_dir}", file=sys.stderr)
