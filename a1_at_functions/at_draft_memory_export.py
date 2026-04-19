# Extracted from C:/!ass-ade/src/ass_ade/cli.py:190
# Component id: at.source.ass_ade.memory_export
__version__ = "0.1.0"

def memory_export(
    output: Path = typer.Argument(Path("atomadic-memory-export.json"), help="Export destination."),
) -> None:
    """Export local memory to a JSON file for backup."""
    import json as _json
    from ass_ade.interpreter import MemoryStore
    store = MemoryStore.load()
    data = store.to_dict()
    output.write_text(_json.dumps(data, indent=2, default=str), encoding="utf-8")
    console.print(f"[green]Memory exported →[/green] {output}")
