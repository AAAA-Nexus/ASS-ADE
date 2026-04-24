"""Tier a2 — assimilated method 'CancellationContext.cancel'

Assimilated from: cancellation.py:25-28
"""

from __future__ import annotations


# --- assimilated symbol ---
def cancel(self) -> None:
    """Mark this context as cancelled."""
    with self._lock:
        self._cancelled = True

