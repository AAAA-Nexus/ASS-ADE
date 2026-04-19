# Extracted from C:/!ass-ade/src/ass_ade/agent/loop.py:108
# Component id: qk.source.ass_ade.token_budget
from __future__ import annotations

__version__ = "0.1.0"

def token_budget(self) -> TokenBudget:
    return self._conversation.budget
