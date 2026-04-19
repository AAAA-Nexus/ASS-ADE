# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trim_to_budget.py:7
# Component id: at.source.a1_at_functions.trim_to_budget
from __future__ import annotations

__version__ = "0.1.0"

def trim_to_budget(self, tools: list[ToolSchema] | None = None) -> int:
    """Trim oldest non-system messages to fit within the token budget.

    Uses the TokenBudget invariant:
        Σ tokens(messages) + tokens(tools) + reserve ≤ context_window

    Returns the number of messages evicted.
    """
    to_evict = self._budget.messages_to_evict(self._messages, tools)
    if to_evict == 0:
        return 0

    system = [m for m in self._messages if m.role == "system"]
    others = [m for m in self._messages if m.role != "system"]

    self._messages = system + others[to_evict:]
    return to_evict
