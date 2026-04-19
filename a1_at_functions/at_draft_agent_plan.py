# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_plan.py:7
# Component id: at.source.a1_at_functions.agent_plan
from __future__ import annotations

__version__ = "0.1.0"

def agent_plan(self, goal: str, **kwargs: Any) -> AgentPlan:
    """/v1/agents/plan — decompose goal into dependency-aware steps. $0.060/request"""
    return self._post_model("/v1/agents/plan", AgentPlan, {"goal": goal, **kwargs})
