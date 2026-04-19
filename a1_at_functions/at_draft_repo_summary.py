# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_repo_summary.py:5
# Component id: at.source.ass_ade.repo_summary
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
