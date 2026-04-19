# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_cancel.py:7
# Component id: at.source.a1_at_functions.cancel
from __future__ import annotations

__version__ = "0.1.0"

def cancel(self) -> None:
    """Mark this context as cancelled."""
    with self._lock:
        self._cancelled = True
