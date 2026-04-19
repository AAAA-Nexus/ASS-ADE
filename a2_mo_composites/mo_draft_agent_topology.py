# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:628
# Component id: mo.source.ass_ade.agent_topology
from __future__ import annotations

__version__ = "0.1.0"

def agent_topology(self, **kwargs: Any) -> AgentTopology:
    """/v1/agents/topology — global swarm topology. $0.008/call"""
    return self._get_model("/v1/agents/topology", AgentTopology, **kwargs)
