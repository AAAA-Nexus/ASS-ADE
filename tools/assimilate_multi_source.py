#!/usr/bin/env python3
"""MAP=TERRAIN generic multi-source assimilation driver.

This does **not** copy source trees verbatim. It runs the monadic book so that
ingestions from a primary root and any number of additional roots merge into
one gap plan (``source_rank`` 0 = primary wins), then materialize/audit/package
as usual.

Environment
-----------
ASS_ADE_SOURCE_ROOTS
    Optional path-list of additional source roots. Uses the platform path
    separator (``;`` on Windows, ``:`` on POSIX).

ASS_ADE_LEGACY_ROOT
    Deprecated compatibility alias for one additional source root.

Example (PowerShell)::

    python tools/assimilate_multi_source.py -o C:\\build\\unified-out --source ..\\!aaaa-nexus-mcp --stop-after gapfill

"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    return slug or "source"


def _env_source_roots() -> list[Path]:
    raw_many = os.environ.get("ASS_ADE_SOURCE_ROOTS", "").strip()
    if raw_many:
        return [Path(part) for part in raw_many.split(os.pathsep) if part.strip()]
    raw_legacy = os.environ.get("ASS_ADE_LEGACY_ROOT", "").strip()
    if raw_legacy:
        return [Path(raw_legacy)]
    return []


def _dedupe_roots(primary: Path, roots: list[Path]) -> list[Path]:
    seen = {primary.resolve()}
    out: list[Path] = []
    for root in roots:
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def _root_ids(primary: Path, sources: list[Path], explicit: list[str] | None) -> list[str]:
    if explicit:
        if len(explicit) != len(sources) + 1:
            raise ValueError("--root-id count must equal primary + source count")
        return explicit
    ids = [_slug(primary.name)]
    used = set(ids)
    for root in sources:
        base = _slug(root.name)
        candidate = base
        i = 2
        while candidate in used:
            candidate = f"{base}_{i}"
            i += 1
        used.add(candidate)
        ids.append(candidate)
    return ids


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
        "--source",
        "--also",
        action="append",
        type=Path,
        default=[],
        help="Additional source root to merge after primary. May be repeated.",
    )
    parser.add_argument(
        "--legacy",
        type=Path,
        default=None,
        help="Deprecated alias for one --source root.",
    )
    parser.add_argument(
        "--root-id",
        action="append",
        default=None,
        help="Explicit root id. Repeat once for primary and once for each source.",
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
        default="assimilated-unified",
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
    sources = list(args.source or [])
    if args.legacy is not None:
        sources.append(args.legacy)
    if not sources:
        sources.extend(_env_source_roots())
    sources = _dedupe_roots(primary, sources)
    if not sources:
        sys.stderr.write(
            "Pass at least one --source/--also root, set ASS_ADE_SOURCE_ROOTS, "
            "or use deprecated ASS_ADE_LEGACY_ROOT.\n"
        )
        return 2
    for source in sources:
        if not source.is_dir():
            sys.stderr.write(f"Source root is not a directory: {source}\n")
            return 2
    try:
        root_ids = _root_ids(primary, sources, args.root_id)
    except ValueError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2

    # Import after path hygiene so ``python tools/...`` works without install.
    sys.path.insert(0, str(primary / "src"))

    from ass_ade.a3_og_features.pipeline_book import run_book_until, stop_after_from_label

    stop_n = stop_after_from_label(args.stop_after)
    book = run_book_until(
        primary,
        args.output,
        stop_after=stop_n,
        rebuild_tag=args.rebuild_tag,
        extra_source_roots=sources,
        root_ids=root_ids,
        task_description="assimilate_multi_source",
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
        "root_ids": root_ids,
        "gap_components": len(
            (book.get("phase2") or {}).get("gap_plan", {}).get("proposed_components") or []
        ),
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
