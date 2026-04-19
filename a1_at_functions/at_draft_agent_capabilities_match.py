# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_capabilities_match.py:7
# Component id: at.source.a1_at_functions.agent_capabilities_match
from __future__ import annotations

__version__ = "0.1.0"

def agent_capabilities_match(self, task: str, **kwargs: Any) -> CapabilityMatch:
    """/v1/agents/capabilities/match — find matching agents in the swarm. $0.020/request"""
    return self._post_model("/v1/agents/capabilities/match", CapabilityMatch, {"task": task, **kwargs})
