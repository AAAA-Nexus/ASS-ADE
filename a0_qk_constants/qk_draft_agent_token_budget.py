# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:644
# Component id: qk.source.ass_ade.agent_token_budget
from __future__ import annotations

__version__ = "0.1.0"

def agent_token_budget(self, task: str, models: list[str] | None = None, **kwargs: Any) -> TokenBudget:
    """/v1/agents/token-budget — cost estimate across 7 models. $0.020/request"""
    return self._post_model("/v1/agents/token-budget", TokenBudget, {"task": task, "models": models or [], **kwargs})
