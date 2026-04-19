# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_hash_command.py:7
# Component id: at.source.a1_at_functions.prompt_hash_command
from __future__ import annotations

__version__ = "0.1.0"

def prompt_hash_command(
    prompt_path: str | None = typer.Argument(None, help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Return SHA-256 metadata for an explicit prompt artifact."""
    from ass_ade.prompt_toolkit import prompt_hash

    try:
        result = prompt_hash(working_dir=path, prompt_path=prompt_path, prompt_text=text)
    except ValueError as exc:
        console.print(f"[red]Prompt hash error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"Source: {result.source}")
        console.print(f"SHA-256: {result.sha256}")
        console.print(f"Bytes: {result.bytes}")
        console.print(f"Lines: {result.lines}")
