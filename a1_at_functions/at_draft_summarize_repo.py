# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_summarize_repo.py:7
# Component id: at.source.a1_at_functions.summarize_repo
from __future__ import annotations

__version__ = "0.1.0"

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
