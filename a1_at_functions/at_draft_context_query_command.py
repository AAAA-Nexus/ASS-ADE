# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3398
# Component id: at.source.ass_ade.context_query_command
from __future__ import annotations

__version__ = "0.1.0"

def context_query_command(
    query: str = typer.Argument(..., help="Query local vector memory."),
    namespace: str = typer.Option("default", help="Memory namespace."),
    top_k: int = typer.Option(5, help="Number of matches to return."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Query the local vector memory."""
    from ass_ade.context_memory import query_vector_memory

    result = query_vector_memory(
        query=query,
        namespace=namespace,
        top_k=top_k,
        working_dir=path,
    )
    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    console.print(f"[green]Matches:[/green] {len(result.matches)}")
    for match in result.matches:
        console.print(f"  - {match.score:.3f} {match.id}: {match.text[:100]}")
