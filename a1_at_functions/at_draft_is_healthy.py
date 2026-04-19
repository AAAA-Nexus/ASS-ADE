# Extracted from C:/!ass-ade/src/ass_ade/nexus/session.py:66
# Component id: at.source.ass_ade.is_healthy
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
