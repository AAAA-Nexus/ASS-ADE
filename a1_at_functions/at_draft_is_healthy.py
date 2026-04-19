# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_is_healthy.py:7
# Component id: at.source.a1_at_functions.is_healthy
from __future__ import annotations

__version__ = "0.1.0"

def is_healthy(self) -> bool:
    """Return True if the session is active and has remaining calls."""
    if not self.is_active:
        return False
    try:
        s = self.status()
        remaining = s.remaining_calls
        return remaining is None or remaining > 0
    except NexusError:
        return False
