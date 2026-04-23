"""Stub LoRA training entry-point — exits cleanly when prerequisites are absent.

Full training pipeline lives in the private Atomadic toolchain.
This stub satisfies `python -m scripts.lora_train` in CI so the workflow
passes until a GPU runner and full dependencies are wired up.
"""

from __future__ import annotations

import argparse
import sys


def _parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="LoRA training stub")
    p.add_argument("--lang", default="python")
    p.add_argument("--profile", default="fast")
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--max-samples", type=int, default=500)
    p.add_argument("--min-samples", type=int, default=20)
    p.add_argument("--upload", default="hf")
    p.add_argument("--hf-repo", default="")
    p.add_argument("--storefront", default="")
    return p.parse_args()


def main() -> None:
    args = _parse()
    print(
        f"lora_train (stub): lang={args.lang} profile={args.profile} "
        f"epochs={args.epochs} max_samples={args.max_samples} — "
        "no training performed (full pipeline requires GPU runner)"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
