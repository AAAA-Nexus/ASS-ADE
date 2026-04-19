# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_context_store_command.py:7
# Component id: mo.source.a2_mo_composites.context_store_command
from __future__ import annotations

__version__ = "0.1.0"

def context_store_command(
    text: str = typer.Argument(..., help="Text to store in local vector memory."),
    namespace: str = typer.Option("default", help="Memory namespace."),
    metadata: str = typer.Option("{}", help="JSON metadata object."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Store text in the local vector memory."""
    from ass_ade.context_memory import store_vector_memory

    try:
        metadata_obj = json.loads(metadata)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Metadata must be JSON:[/red] {exc}")
        raise typer.Exit(code=4) from exc
    if not isinstance(metadata_obj, dict):
        console.print("[red]Metadata must be a JSON object.[/red]")
        raise typer.Exit(code=4)

    result = store_vector_memory(
        text=text,
        namespace=namespace,
        metadata=metadata_obj,
        working_dir=path,
    )
    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"[green]Stored vector memory:[/green] {result.id}")
        console.print(f"Namespace: {result.namespace}")
