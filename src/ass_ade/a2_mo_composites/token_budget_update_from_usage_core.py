"""Tier a2 — assimilated method 'TokenBudget.update_from_usage'

Assimilated from: tokens.py:200-206
"""

from __future__ import annotations


# --- assimilated symbol ---
def update_from_usage(self, usage: dict[str, int] | None) -> None:
    """Update running totals from a completion response's usage dict."""
    if not usage:
        return
    self.prompt_tokens = usage.get("prompt_tokens", self.prompt_tokens)
    self.completion_tokens += usage.get("completion_tokens", 0)
    self.total_calls += 1

