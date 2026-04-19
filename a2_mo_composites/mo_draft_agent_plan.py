# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:654
# Component id: mo.source.ass_ade.agent_plan
from __future__ import annotations

__version__ = "0.1.0"

def agent_plan(self, goal: str, **kwargs: Any) -> AgentPlan:
    """/v1/agents/plan — decompose goal into dependency-aware steps. $0.060/request"""
    return self._post_model("/v1/agents/plan", AgentPlan, {"goal": goal, **kwargs})
