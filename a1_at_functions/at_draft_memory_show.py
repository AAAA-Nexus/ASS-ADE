# Extracted from C:/!ass-ade/src/ass_ade/cli.py:170
# Component id: at.source.ass_ade.memory_show
from __future__ import annotations

__version__ = "0.1.0"

def memory_show() -> None:
    """Show what Atomadic remembers about you and your projects."""
    from ass_ade.interpreter import MemoryStore
    store = MemoryStore.load()
    console.print(store.summarize())
