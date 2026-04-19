# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:616
# Component id: mo.source.ass_ade.discovery_registry
from __future__ import annotations

__version__ = "0.1.0"

def discovery_registry(self, **kwargs: Any) -> AgentRegistry:
    """/v1/discovery/registry — browse all registered agents. $0.020/call"""
    return self._get_model("/v1/discovery/registry", AgentRegistry, **kwargs)
