# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_repo_summary.py:7
# Component id: at.source.a1_at_functions.repo_summary
from __future__ import annotations

__version__ = "0.1.0"

def repo_summary(
    path: Path = REPO_PATH_ARGUMENT,
    top: int = typer.Option(8, min=1, max=25, help="Number of file types to show."),
) -> None:
    summary = summarize_repo(path)

    overview = Table(title="Repo Summary")
    overview.add_column("Signal")
    overview.add_column("Value")
    overview.add_row("Root", str(summary.root))
    overview.add_row("Files", str(summary.total_files))
    overview.add_row("Directories", str(summary.total_dirs))
    overview.add_row("Top-level Entries", ", ".join(summary.top_level_entries[:12]) or "none")
    console.print(overview)

    types = Table(title="Top File Types")
    types.add_column("Type")
    types.add_column("Count", justify="right")
    for file_type, count in list(summary.file_types.items())[:top]:
        types.add_row(file_type, str(count))
    console.print(types)
