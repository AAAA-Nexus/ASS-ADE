"""Detect Python module stem collisions across multiple source roots (MAP=TERRAIN)."""

from __future__ import annotations

import fnmatch
import hashlib
import os
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.exclude_dirs import is_excluded_dir_name
from ass_ade.a0_qk_constants.policy_types import RootPolicy

_SKIP_STEMS = frozenset({"__init__", "conftest", "setup", "manage"})
_SKIP_PREFIXES = ("test_", "qk_draft_", "at_draft_", "mo_draft_", "og_draft_", "sy_draft_")


def _matches_any(posix_rel: str, patterns: tuple[str, ...]) -> bool:
    for pat in patterns:
        if fnmatch.fnmatch(posix_rel, pat):
            return True
        if pat.startswith("**/") and fnmatch.fnmatch(posix_rel, pat[3:]):
            return True
    return False


def _file_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except OSError:
        return ""


def detect_namespace_conflicts(
    source_paths: list[Path],
    *,
    policy_by_root: dict[Path, RootPolicy] | None = None,
) -> dict[str, Any]:
    """Flag same module stem in 2+ roots with different content hashes."""
    stem_registry: dict[str, list[tuple[str, str]]] = {}

    for src_root in source_paths:
        if not src_root.is_dir():
            continue
        root_resolved = src_root.resolve()
        row = policy_by_root.get(root_resolved) if policy_by_root else None
        forbids: tuple[str, ...] = row["forbid_globs"] if row and row.get("forbid_globs") else ()
        py_files: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(root_resolved):
            dirnames[:] = [n for n in dirnames if not is_excluded_dir_name(n)]
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                py_files.append(Path(dirpath) / filename)
        for py_file in sorted(py_files):
            if forbids:
                try:
                    rel = py_file.resolve().relative_to(root_resolved).as_posix()
                except ValueError:
                    rel = py_file.name
                if _matches_any(rel, forbids):
                    continue
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
