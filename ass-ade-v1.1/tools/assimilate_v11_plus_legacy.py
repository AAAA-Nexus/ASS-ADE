#!/usr/bin/env python3
"""MAP=TERRAIN dual-source driver: primary ``ass-ade-v1.1`` + secondary full ``!ass-ade``.

This does **not** copy the legacy tree verbatim; it runs the v1.1 monadic book so that
ingestions from both roots merge into one gap plan (``source_rank`` 0 = primary wins),
then materialize/audit/package as usual. For a full product merge, also plan vendoring of
``ass_ade`` package layout and CLI entrypoints (separate step).

Environment
-----------
ASS_ADE_LEGACY_ROOT
    Absolute path to the legacy ASS-ADE repo root (the tree that contains ``src/ass_ade``).

Example (PowerShell)::

    $env:ASS_ADE_LEGACY_ROOT = 'C:\\!aaaa-nexus\\!ass-ade'
    python tools/assimilate_v11_plus_legacy.py -o C:\\build\\unified-out --stop-after gapfill

"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output parent (required for materialize+).",
    )
    parser.add_argument(
        "--primary",
        type=Path,
        default=None,
        help="Primary source root (default: this repository).",
    )
    parser.add_argument(
        "--legacy",
        type=Path,
        default=None,
        help="Secondary legacy root (default: ASS_ADE_LEGACY_ROOT env).",
    )
    parser.add_argument(
        "--stop-after",
        default="package",
        help="Phase label: recon, ingest, gapfill, enrich, validate, materialize, audit, package.",
    )
    parser.add_argument(
        "--rebuild-tag",
        default=None,
        help="Tag directory under output (default: UTC timestamp).",
    )
    parser.add_argument(
        "--distribution-name",
        default="ass-ade-assimilated-unified",
        help="Phase 7 pyproject [project] name.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write full book JSON to this path.",
    )
    args = parser.parse_args()

    primary = (args.primary or _repo_root()).resolve()
    legacy = args.legacy
    if legacy is None:
        raw = os.environ.get("ASS_ADE_LEGACY_ROOT", "").strip()
        if not raw:
            sys.stderr.write(
                "Set ASS_ADE_LEGACY_ROOT or pass --legacy to the full !ass-ade checkout.\n"
            )
            return 2
        legacy = Path(raw)
    legacy = legacy.resolve()
    if not legacy.is_dir():
        sys.stderr.write(f"Legacy root is not a directory: {legacy}\n")
        return 2

    # Import after path hygiene so ``python tools/...`` works without install
    sys.path.insert(0, str(primary / "src"))

    from ass_ade_v11.a3_og_features.pipeline_book import run_book_until, stop_after_from_label

    stop_n = stop_after_from_label(args.stop_after)
    book = run_book_until(
        primary,
        args.output,
        stop_after=stop_n,
        rebuild_tag=args.rebuild_tag,
        extra_source_roots=[legacy],
        root_ids=["ass_ade_v11", "ass_ade_legacy"],
        task_description="assimilate_v11_plus_legacy",
        distribution_name=args.distribution_name,
    )

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(book, indent=2, default=str) + "\n", encoding="utf-8")

    summary = {
        "stopped_after": book.get("stopped_after"),
        "rebuild_tag": book.get("rebuild_tag"),
        "verdict": (book.get("phase0") or {}).get("verdict"),
        "sources": len((book.get("phase0") or {}).get("source_roots") or []),
        "gap_components": len((book.get("phase2") or {}).get("gap_plan", {}).get("proposed_components") or []),
    }
    print(json.dumps(summary, indent=2))

    p0 = book.get("phase0") or {}
    if p0.get("verdict") != "READY_FOR_PHASE_1" and stop_n > 0:
        return 1
    if stop_n >= 6:
        audit = (book.get("phase6") or {}).get("audit") or {}
        summary_a = audit.get("summary") or {}
        if not summary_a.get("structure_conformant"):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
