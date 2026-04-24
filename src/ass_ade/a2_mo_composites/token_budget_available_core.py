"""Tier a2 — assimilated method 'TokenBudget.available'

Assimilated from: tokens.py:189-191
"""

from __future__ import annotations


# --- assimilated symbol ---
def available(self) -> int:
    """Tokens available for prompt content (messages + tools)."""
    return max(0, self.context_window - self.reserve)

