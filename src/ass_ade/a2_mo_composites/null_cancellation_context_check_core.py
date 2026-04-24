"""Tier a2 — assimilated method 'NullCancellationContext.check'

Assimilated from: cancellation.py:53-55
"""

from __future__ import annotations


# --- assimilated symbol ---
def check(self) -> bool:
    """Always return False — never cancelled."""
    return False

