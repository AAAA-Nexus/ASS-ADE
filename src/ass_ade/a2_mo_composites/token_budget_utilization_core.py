"""Tier a2 — assimilated method 'TokenBudget.utilization'

Assimilated from: tokens.py:194-198
"""

from __future__ import annotations


# --- assimilated symbol ---
def utilization(self) -> float:
    """Fraction of context window currently used (0.0 – 1.0)."""
    if self.context_window == 0:
        return 1.0
    return min(1.0, self.prompt_tokens / self.context_window)

