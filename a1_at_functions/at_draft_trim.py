# Extracted from C:/!ass-ade/src/ass_ade/agent/conversation.py:61
# Component id: at.source.ass_ade.trim
from __future__ import annotations

__version__ = "0.1.0"

def trim(self, max_messages: int = 50) -> int:
    """Trim oldest non-system messages if over limit. Returns count removed."""
    if len(self._messages) <= max_messages:
        return 0

    system = [m for m in self._messages if m.role == "system"]
    others = [m for m in self._messages if m.role != "system"]

    keep = max_messages - len(system)
    removed = len(others) - keep
    if removed <= 0:
        return 0

    self._messages = system + others[removed:]
    return removed
