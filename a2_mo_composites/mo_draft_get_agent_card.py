# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:281
# Component id: mo.source.ass_ade.get_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def get_agent_card(self) -> AgentCard:
    """/.well-known/agent.json — A2A capability manifest, free"""
    return self._get_model("/.well-known/agent.json", AgentCard)
