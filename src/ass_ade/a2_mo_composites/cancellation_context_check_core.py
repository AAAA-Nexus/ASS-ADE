"""Tier a2 — assimilated method 'CancellationContext.check'

Assimilated from: cancellation.py:30-38
"""

from __future__ import annotations


# --- assimilated symbol ---
def check(self) -> bool:
    """Check if cancellation has been requested.

    Returns True if cancel() was called, False otherwise.
    Long-running operations should call this periodically and exit early
    if it returns True.
    """
    with self._lock:
        return self._cancelled

