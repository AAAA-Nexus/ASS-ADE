"""Conflict Detector — detect module name collisions across multi-source rebuilds.

Runs between Phase 1 (Ingest) and Phase 2 (Gap-Fill) in the rebuild orchestrator.

Problem: when two source projects both provide a `utils.py` (or `config.py`,
`errors.py`, etc.) with different content, the current rebuild engine silently
lets the last one win at materialize time. This produces invisible data loss.

This module detects that BEFORE materialize and surfaces it in the phases dict
so users can decide how to resolve the conflict (rename, merge, promote to tools/).
"""
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


def detect_namespace_conflicts(
    source_paths: list[Path],
) -> dict[str, Any]:
    """Scan all source paths for Python module name collisions with different content.

    Only flags files whose stems appear in 2+ source roots with diverging content
    hashes — identical copies (vendored deps, shared utils) are not flagged.

    Args:
        source_paths: Ordered list of source root directories (as passed to rebuild).

    Returns:
        {
            "conflicts": [
                {
                    "stem":       "utils",
                    "sources":    ["/proj-a/utils.py", "/proj-b/utils.py"],
                    "hashes":     ["abc123", "def456"],
                    "resolution": "last_wins",
                }
            ],
            "conflict_count": N,
            "clean":          True | False,
        }
    """
    # stem → list of (abs_path_str, hash) from each source root
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
                "stem":       stem,
                "sources":    [p for p, _ in entries],
                "hashes":     [h for _, h in entries],
                "resolution": "last_wins",
            })

    return {
        "conflicts":      conflicts,
        "conflict_count": len(conflicts),
        "clean":          len(conflicts) == 0,
    }


def format_conflict_report(result: dict[str, Any]) -> str:
    """Return a human-readable conflict summary for CLI display."""
    conflicts = result.get("conflicts", [])
    if not conflicts:
        return "[ok] No module name conflicts detected."

    lines = [f"[warn] {len(conflicts)} namespace conflict(s) detected — rebuild used last_wins:"]
    for c in conflicts:
        lines.append(f"  • {c['stem']}.py  ({len(c['sources'])} versions, hashes: {', '.join(c['hashes'])})")
        for src in c["sources"]:
            lines.append(f"      {src}")
        lines.append(f"    -> Resolution: {c['resolution']}  (last source path wins at materialize)")
    lines.append("")
    lines.append("  Tip: add a REBUILD_MANIFEST.json to promote shared utilities to tools/.")
    return "\n".join(lines)
