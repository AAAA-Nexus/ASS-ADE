# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3179
# Component id: at.source.ass_ade.prompt_validate_command
__version__ = "0.1.0"

def prompt_validate_command(
    manifest_path: str = typer.Argument(..., help="Prompt manifest JSON file."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    prompt_name: str | None = typer.Option(None, help="Optional manifest prompt entry name."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Validate an explicit prompt artifact against a JSON hash manifest."""
    from ass_ade.prompt_toolkit import prompt_validate

    try:
        result = prompt_validate(
            manifest_path=manifest_path,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
            prompt_name=prompt_name,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt validation error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        color = "green" if result.valid else "red"
        console.print(f"[{color}]Valid: {result.valid}[/{color}]")
        console.print(f"Source: {result.source}")
        console.print(f"SHA-256: {result.sha256}")
