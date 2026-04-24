"""Tier a2 — assimilated method 'CancellationContext.__init__'

Assimilated from: cancellation.py:21-23
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(self) -> None:
    self._cancelled = False
    self._lock = threading.Lock()

