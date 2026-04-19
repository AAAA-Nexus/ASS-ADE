# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3274
# Component id: at.source.ass_ade.prompt_propose_command
__version__ = "0.1.0"

def prompt_propose_command(
    objective: str = typer.Argument(..., help="Prompt improvement objective."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Create a prompt self-improvement proposal."""
    from ass_ade.prompt_toolkit import prompt_propose

    try:
        result = prompt_propose(
            objective=objective,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt proposal error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"Proposal: {result.proposal_id}")
        for change in result.recommended_changes:
            console.print(f"  - {change}")
