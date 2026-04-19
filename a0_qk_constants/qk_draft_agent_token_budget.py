# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_agent_token_budget.py:7
# Component id: qk.source.a0_qk_constants.agent_token_budget
from __future__ import annotations

__version__ = "0.1.0"

def agent_token_budget(self, task: str, models: list[str] | None = None, **kwargs: Any) -> TokenBudget:
    """/v1/agents/token-budget — cost estimate across 7 models. $0.020/request"""
    return self._post_model("/v1/agents/token-budget", TokenBudget, {"task": task, "models": models or [], **kwargs})
