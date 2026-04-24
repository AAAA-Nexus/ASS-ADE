"""Tier a2 — assimilated class 'NullCancellationContext'

Assimilated from: cancellation.py:46-55
"""

from __future__ import annotations


# --- assimilated symbol ---
class NullCancellationContext(CancellationContext):
    """No-op cancellation context for operations that don't support cancellation."""

    def cancel(self) -> None:
        """Do nothing."""
        pass

    def check(self) -> bool:
        """Always return False — never cancelled."""
        return False

