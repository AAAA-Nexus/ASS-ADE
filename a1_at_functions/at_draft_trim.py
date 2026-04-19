# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trim.py:7
# Component id: at.source.a1_at_functions.trim
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
