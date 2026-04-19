# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_agent_card.py:7
# Component id: at.source.a1_at_functions.get_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def get_agent_card(self) -> AgentCard:
    """/.well-known/agent.json — A2A capability manifest, free"""
    return self._get_model("/.well-known/agent.json", AgentCard)
