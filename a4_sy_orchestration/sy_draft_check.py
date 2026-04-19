# Extracted from C:/!ass-ade/src/ass_ade/mcp/cancellation.py:30
# Component id: sy.source.ass_ade.check
from __future__ import annotations

__version__ = "0.1.0"

def check(self) -> bool:
    """Check if cancellation has been requested.

    Returns True if cancel() was called, False otherwise.
    Long-running operations should call this periodically and exit early
    if it returns True.
    """
    with self._lock:
        return self._cancelled
