"""Pure repository surface statistics for Phase 0 recon."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.exclude_dirs import is_excluded_dir_name


def _walk_top_level_dirs(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    out: list[str] = []
    try:
        for child in sorted(root.iterdir()):
            if child.is_dir() and not is_excluded_dir_name(child.name) and not child.name.startswith("."):
                out.append(child.name)
    except OSError:
        return []
    return out


def compute_repo_surface(root: Path) -> dict[str, Any]:
    """Return counts and markers used to decide Phase 0 verdict."""
    root = root.resolve()
    py_files = 0
    total_files = 0
    if root.is_dir():
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not is_excluded_dir_name(d)]
            for name in filenames:
                total_files += 1
                if name.endswith(".py"):
                    py_files += 1
    has_pyproject = (root / "pyproject.toml").is_file()
    return {
        "root": root.as_posix(),
        "total_files": total_files,
        "python_files": py_files,
        "has_pyproject_toml": has_pyproject,
        "top_level_dirs": _walk_top_level_dirs(root),
    }
