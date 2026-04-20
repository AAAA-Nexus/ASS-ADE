#!/usr/bin/env python3
"""Apply enhancement fixes for one evolution lane.

Usage
-----
    python3 scripts/apply_fixes.py <max_apply> [--lane LANE] [--scan-file PATH] [--root DIR]

Reads the pre-filtered ``enhance_scan.json`` written by the workflow's Phase 2
context step, applies up to *max_apply* fixes via ``apply_enhancement()``, and
writes ``apply_summary.json`` for downstream steps to consume.

Exit code is always 0 — individual fix failures are non-fatal.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_scan(scan_file: Path) -> list[dict]:
    if not scan_file.exists():
        print(f"No scan file at {scan_file} — nothing to apply", file=sys.stderr)
        return []
    try:
        data = json.loads(scan_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Could not parse {scan_file}: {exc}", file=sys.stderr)
        return []
    return data.get("findings", [])


def _write_summary(summary_path: Path, lane: str, applied: list[str], skipped: list[str]) -> None:
    summary_path.write_text(
        json.dumps({"lane": lane, "applied": applied, "skipped": skipped}, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("max_apply", type=int, help="Maximum number of fixes to apply")
    parser.add_argument("--lane", default="general", help="Evolution lane name")
    parser.add_argument("--scan-file", default="enhance_scan.json", help="Path to filtered findings JSON")
    parser.add_argument("--root", default=".", help="Repo root directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    scan_file = Path(args.scan_file)
    summary_path = root / "apply_summary.json"

    findings = _load_scan(scan_file)
    if not findings:
        print(f"Lane={args.lane} Applied=0 Skipped=0 (no findings)")
        _write_summary(summary_path, args.lane, [], [])
        return 0

    sys.path.insert(0, str(root / "src"))
    try:
        from ass_ade.local.enhancer import apply_enhancement
    except ImportError as exc:
        print(f"Could not import apply_enhancement: {exc}", file=sys.stderr)
        _write_summary(summary_path, args.lane, [], [])
        return 0

    applied: list[str] = []
    skipped: list[str] = []

    for finding in findings[: args.max_apply]:
        label = f"{finding.get('category', '?')} in {finding.get('file', '?')}"
        try:
            ok = apply_enhancement(root, finding)
            if ok:
                applied.append(label)
            else:
                skipped.append(label)
        except Exception as exc:  # noqa: BLE001
            skipped.append(f"{label} ({exc})")

    print(f"Lane={args.lane} Applied={len(applied)} Skipped={len(skipped)}")
    for a in applied:
        print(f"  + {a}")
    for s in skipped:
        print(f"  - {s}")

    _write_summary(summary_path, args.lane, applied, skipped)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
