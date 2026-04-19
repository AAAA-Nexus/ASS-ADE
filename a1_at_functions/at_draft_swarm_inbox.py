# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_swarm_inbox.py:7
# Component id: at.source.a1_at_functions.swarm_inbox
from __future__ import annotations

__version__ = "0.1.0"

def swarm_inbox(self, agent_id: str, **kwargs: Any) -> SwarmRelayResult:
    """/v1/swarm/inbox — agent message inbox. $0.008/call"""
    return self._get_model("/v1/swarm/inbox", SwarmRelayResult, agent_id=agent_id, **kwargs)
