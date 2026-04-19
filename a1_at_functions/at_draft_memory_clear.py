# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_memory_clear.py:7
# Component id: at.source.a1_at_functions.memory_clear
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
