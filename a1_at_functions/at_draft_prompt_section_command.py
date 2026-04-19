# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3212
# Component id: at.source.ass_ade.prompt_section_command
__version__ = "0.1.0"

def prompt_section_command(
    section: str = typer.Argument(..., help="Markdown heading or XML tag name."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Extract a prompt section from an explicit prompt artifact."""
    from ass_ade.prompt_toolkit import prompt_section

    try:
        result = prompt_section(
            section=section,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt section error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    elif result.found:
        console.print(result.text, markup=False)
    else:
        console.print("[yellow]Section not found.[/yellow]")
