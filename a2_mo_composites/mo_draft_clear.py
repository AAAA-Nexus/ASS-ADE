# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorystore.py:60
# Component id: mo.source.a2_mo_composites.clear
from __future__ import annotations

__version__ = "0.1.0"

def clear(cls) -> None:
    for filename in [
        "user_profile.json", "project_contexts.json",
        "preferences.json", "conversation_history.jsonl",
    ]:
        p = _MEMORY_DIR / filename
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass
