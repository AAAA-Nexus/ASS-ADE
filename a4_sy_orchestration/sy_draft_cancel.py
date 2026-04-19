# Extracted from C:/!ass-ade/src/ass_ade/mcp/cancellation.py:25
# Component id: sy.source.ass_ade.cancel
from __future__ import annotations

__version__ = "0.1.0"

def cancel(self) -> None:
    """Mark this context as cancelled."""
    with self._lock:
        self._cancelled = True
