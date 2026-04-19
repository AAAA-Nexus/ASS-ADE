# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_protocol_evolution_demo.py:5
# Component id: at.source.ass_ade.protocol_evolution_demo
__version__ = "0.1.0"

def protocol_evolution_demo(
    path: Path = REPO_PATH_OPTION,
    branches: str = typer.Option(
        "tests-first,docs-first,safety-first",
        "--branches",
        help="Comma-separated branch track names.",
    ),
    iterations: int = typer.Option(3, min=1, max=12, help="Iterations to show per branch."),
    output: Path | None = typer.Option(None, "--output", help="Where to write the demo markdown."),
    write: bool = typer.Option(True, "--write/--print", help="Write docs/evolution-workflow.md or print markdown."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON when writing."),
) -> None:
    """Generate the split-branch evolution demo workflow."""
    branch_list = [item.strip() for item in branches.split(",") if item.strip()]
    if not write:
        console.print(render_branch_evolution_demo(root=path, branches=branch_list, iterations=iterations))
        return

    target = write_branch_evolution_demo(
        root=path,
        branches=branch_list,
        iterations=iterations,
        output=output,
    )
    if json_out:
        _print_json({"path": str(target), "branches": branch_list, "iterations": iterations})
    else:
        console.print(f"[green]Wrote evolution demo:[/green] {target}")
