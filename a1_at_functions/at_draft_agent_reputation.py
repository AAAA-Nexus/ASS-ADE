# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_reputation.py:7
# Component id: at.source.a1_at_functions.agent_reputation
from __future__ import annotations

__version__ = "0.1.0"

def agent_reputation(self, agent_id: str, **kwargs: Any) -> dict:
    """/v1/agents/reputation — A2A compliance + trust score. $0.040/request"""
    return self._post_raw("/v1/agents/reputation", {"agent_id": agent_id, **kwargs})
