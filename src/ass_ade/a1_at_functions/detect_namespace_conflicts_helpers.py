"""Tier a1 — assimilated function 'detect_namespace_conflicts'

Assimilated from: rebuild/conflict_detector.py:44-104
"""

from __future__ import annotations


# --- assimilated symbol ---
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
            if _is_excluded_file(py_file, src_root):
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

