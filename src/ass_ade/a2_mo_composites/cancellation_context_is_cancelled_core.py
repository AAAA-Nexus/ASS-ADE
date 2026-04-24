"""Tier a2 — assimilated method 'CancellationContext.is_cancelled'

Assimilated from: cancellation.py:41-43
"""

from __future__ import annotations


# --- assimilated symbol ---
def is_cancelled(self) -> bool:
    """Alias for check()."""
    return self.check()

