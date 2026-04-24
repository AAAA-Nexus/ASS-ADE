from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

DEFAULT_IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "target",
    ".pytest_cache",
    ".pytest_tmp",
    ".ruff_cache",
    "build",
    "dist",
    "examples",
    "benchmarks",
}


@dataclass(frozen=True)
class RepoSummary:
    root: Path
    total_files: int
    total_dirs: int
    file_types: dict[str, int]
    top_level_entries: list[str]


def summarize_repo(root: Path, ignored_dirs: set[str] | None = None) -> RepoSummary:
    root = root.resolve()
    ignores = ignored_dirs or DEFAULT_IGNORED_DIRS
    file_types: Counter[str] = Counter()
    total_files = 0
    total_dirs = 0

    top_level_entries = sorted(item.name for item in root.iterdir()) if root.exists() else []

    for _, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [directory for directory in dirs if directory not in ignores]
        total_dirs += len(dirs)

        for filename in files:
            total_files += 1
            suffix = Path(filename).suffix.lower().lstrip(".") or "[no_ext]"
            file_types[suffix] += 1

    return RepoSummary(
        root=root,
        total_files=total_files,
        total_dirs=total_dirs,
        file_types=dict(file_types.most_common()),
        top_level_entries=top_level_entries,
    )
