# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:242
# Component id: at.source.ass_ade.clear
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
