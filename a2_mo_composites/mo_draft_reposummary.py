# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/repo.py:27
# Component id: mo.source.ass_ade.reposummary
__version__ = "0.1.0"

class RepoSummary:
    root: Path
    total_files: int
    total_dirs: int
    file_types: dict[str, int]
    top_level_entries: list[str]
