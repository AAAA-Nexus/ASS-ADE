# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:433
# Component id: mo.source.a2_mo_composites.agent_topology
from __future__ import annotations

__version__ = "0.1.0"

def agent_topology(self, **kwargs: Any) -> AgentTopology:
    """/v1/agents/topology — global swarm topology. $0.008/call"""
    return self._get_model("/v1/agents/topology", AgentTopology, **kwargs)
