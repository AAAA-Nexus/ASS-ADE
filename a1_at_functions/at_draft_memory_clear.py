# Extracted from C:/!ass-ade/src/ass_ade/cli.py:178
# Component id: at.source.ass_ade.memory_clear
from __future__ import annotations

__version__ = "0.1.0"

def memory_clear(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
) -> None:
    """Wipe all local Atomadic memory."""
    if not confirm:
        typer.confirm("This will erase all local Atomadic memory. Continue?", abort=True)
    from ass_ade.interpreter import MemoryStore
    MemoryStore.clear()
    console.print("[green]Memory cleared.[/green]")
