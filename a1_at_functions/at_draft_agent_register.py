# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_register.py:7
# Component id: at.source.a1_at_functions.agent_register
from __future__ import annotations

__version__ = "0.1.0"

def agent_register(self, agent_id: int, name: str, capabilities: list[str], endpoint: str, **kwargs: Any) -> AgentRegistration:
    """POST /v1/agents/register — agent_id must be a multiple of G_18 (324). Free"""
    return self._post_model("/v1/agents/register", AgentRegistration, {
        "agent_id": agent_id, "name": name, "capabilities": capabilities, "endpoint": endpoint, **kwargs,
    })
