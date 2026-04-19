# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:459
# Component id: mo.source.a2_mo_composites.agent_plan
from __future__ import annotations

__version__ = "0.1.0"

def agent_plan(self, goal: str, **kwargs: Any) -> AgentPlan:
    """/v1/agents/plan — decompose goal into dependency-aware steps. $0.060/request"""
    return self._post_model("/v1/agents/plan", AgentPlan, {"goal": goal, **kwargs})
