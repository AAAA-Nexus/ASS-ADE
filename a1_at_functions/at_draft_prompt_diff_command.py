# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3243
# Component id: at.source.ass_ade.prompt_diff_command
from __future__ import annotations

__version__ = "0.1.0"

def prompt_diff_command(
    baseline_path: str = typer.Argument(..., help="Baseline prompt file."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Current prompt file."),
    text: str | None = typer.Option(None, "--text", help="Inline current prompt text."),
    path: Path = REPO_PATH_OPTION,
    redacted: bool = typer.Option(True, "--redacted/--raw", help="Redact secrets in diff."),
    max_lines: int = typer.Option(200, help="Maximum diff lines."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Compare a prompt artifact to a baseline with redaction."""
    from ass_ade.prompt_toolkit import prompt_diff

    try:
        result = prompt_diff(
            baseline_path=baseline_path,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
            redacted=redacted,
            max_lines=max_lines,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt diff error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(result.diff, markup=False)
