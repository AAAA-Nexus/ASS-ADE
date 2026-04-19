# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:640
# Component id: mo.source.ass_ade.agent_reputation
from __future__ import annotations

__version__ = "0.1.0"

def agent_reputation(self, agent_id: str, **kwargs: Any) -> dict:
    """/v1/agents/reputation — A2A compliance + trust score. $0.040/request"""
    return self._post_raw("/v1/agents/reputation", {"agent_id": agent_id, **kwargs})
