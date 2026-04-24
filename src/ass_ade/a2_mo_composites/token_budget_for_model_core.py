"""Tier a2 — assimilated method 'TokenBudget.for_model'

Assimilated from: tokens.py:185-186
"""

from __future__ import annotations


# --- assimilated symbol ---
def for_model(cls, model: str | None) -> TokenBudget:
    return cls(context_window=context_window_for(model))

