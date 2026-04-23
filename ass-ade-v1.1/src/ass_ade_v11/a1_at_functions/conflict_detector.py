"""Detect Python module stem collisions across multiple source roots (MAP=TERRAIN)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

_SKIP_STEMS = frozenset({"__init__", "conftest", "setup", "manage"})
_SKIP_PREFIXES = ("test_", "qk_draft_", "at_draft_", "mo_draft_", "og_draft_", "sy_draft_")


def _file_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except OSError:
        return ""


def detect_namespace_conflicts(source_paths: list[Path]) -> dict[str, Any]:
    """Flag same module stem in 2+ roots with different content hashes."""
    stem_registry: dict[str, list[tuple[str, str]]] = {}

    for src_root in source_paths:
        if not src_root.is_dir():
            continue
        for py_file in sorted(src_root.rglob("*.py")):
            stem = py_file.stem
            if stem in _SKIP_STEMS:
                continue
            if any(stem.startswith(p) for p in _SKIP_PREFIXES):
                continue
            fhash = _file_hash(py_file)
            if fhash:
                stem_registry.setdefault(stem, []).append((str(py_file), fhash))

    conflicts: list[dict[str, Any]] = []
    for stem, entries in sorted(stem_registry.items()):
        if len(entries) < 2:
            continue
        unique_hashes = {h for _, h in entries}
        if len(unique_hashes) > 1:
            conflicts.append({
                "stem": stem,
                "sources": [p for p, _ in entries],
                "hashes": [h for _, h in entries],
                "resolution": "primary_wins",
            })

    return {
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "clean": len(conflicts) == 0,
    }


def format_conflict_report(result: dict[str, Any]) -> str:
    conflicts = result.get("conflicts", [])
    if not conflicts:
        return "[ok] No module name conflicts detected."

    lines = [
        f"[warn] {len(conflicts)} namespace conflict(s) — primary source wins on duplicate symbols:",
    ]
    for c in conflicts:
        lines.append(
            f"  • {c['stem']}.py  ({len(c['sources'])} versions, hashes: {', '.join(c['hashes'])})"
        )
        for src in c["sources"]:
            lines.append(f"      {src}")
    return "\n".join(lines)
