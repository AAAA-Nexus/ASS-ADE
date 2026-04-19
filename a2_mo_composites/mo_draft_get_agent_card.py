# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:86
# Component id: mo.source.a2_mo_composites.get_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def get_agent_card(self) -> AgentCard:
    """/.well-known/agent.json — A2A capability manifest, free"""
    return self._get_model("/.well-known/agent.json", AgentCard)
