#!/usr/bin/env python3
"""Build a JSONL corpus from ASS-ADE monorepo dev artifacts (LoRA / CLM-friendly).

Each line is one JSON object: {"text": "...", "source": "relative/path"}.

Usage (repo root):
  python scripts/collect_ass_ade_dev_corpus.py
  python scripts/collect_ass_ade_dev_corpus.py --out training_data/ass_ade_dev.jsonl --max-files 800

Does not upload anywhere. Pair with Nexus MCP governance on generations separately;
optional downstream: HuggingFace datasets, PEFT, or Atomadic ``lora-train`` when that
pipeline is available in your environment.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


_SKIP_DIR_PARTS = frozenset(
    {
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        ".import_linter_cache",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".pytest_tmp",
        "rebuild-outputs",
    }
)


def _skip_path(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    for part in rel.parts:
        if part in _SKIP_DIR_PARTS:
            return True
        pl = part.lower()
        if "backup" in pl or pl.endswith("_tmp"):
            return True
    return False


def _iter_files(root: Path, roots: list[Path], suffixes: frozenset[str]) -> list[Path]:
    out: list[Path] = []
    for base in roots:
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if _skip_path(p, root):
                continue
            if p.suffix.lower() not in suffixes:
                continue
            out.append(p)
    out.sort(key=lambda x: str(x))
    return out


def _read_capped(path: Path, max_bytes: int) -> str:
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[:max_bytes] + b"\n\n[... truncated by collect_ass_ade_dev_corpus ...]\n"
    return data.decode("utf-8", errors="replace")


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect ASS-ADE dev text into JSONL for training.")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSONL path (default: training_data/ass_ade_dev.jsonl under repo root).",
    )
    ap.add_argument("--max-files", type=int, default=600, help="Cap number of files scanned.")
    ap.add_argument(
        "--max-bytes",
        type=int,
        default=120_000,
        help="Max bytes read per file (excess truncated).",
    )
    args = ap.parse_args()

    root = _repo_root()
    out = Path(args.out) if args.out else (root / "training_data" / "ass_ade_dev.jsonl")
    out = (out if out.is_absolute() else (Path.cwd() / out)).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    scan_roots = [
        root / "ass-ade-v1.1" / "src" / "ass_ade_v11",
        root / "agents",
        root / "docs",
        root / "ADE",
        root / ".ato-plans" / "active" / "ass-ade-ship-nexus-github-20260422",
    ]
    suffixes = frozenset({".py", ".md", ".mdc", ".toml"})
    files = _iter_files(root, scan_roots, suffixes)[: args.max_files]

    n = 0
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for path in files:
            rel = path.relative_to(root).as_posix()
            body = _read_capped(path, args.max_bytes)
            text = f"# {rel}\n\n{body}"
            rec = {"source": rel, "text": text}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1

    try:
        rel = out.relative_to(root.resolve())
    except ValueError:
        rel = out
    print(f"Wrote {n} records to {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
