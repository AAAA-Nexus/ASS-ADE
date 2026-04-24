"""Tier a2 — assimilated method 'Priority.rank'

Assimilated from: types.py:31-33
"""

from __future__ import annotations


# --- assimilated symbol ---
def rank(self) -> int:
    """Lower rank = higher urgency. Used for inbox ordering."""
    return {"P0-halt": 0, "P1-reroute": 1, "P2-inform": 2, "P3-fyi": 3}[self.value]

