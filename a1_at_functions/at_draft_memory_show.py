# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_memory_show.py:7
# Component id: at.source.a1_at_functions.memory_show
from __future__ import annotations

__version__ = "0.1.0"

def memory_show() -> None:
    """Show what Atomadic remembers about you and your projects."""
    from ass_ade.interpreter import MemoryStore
    store = MemoryStore.load()
    console.print(store.summarize())
