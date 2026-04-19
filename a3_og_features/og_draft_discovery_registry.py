# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_discovery_registry.py:7
# Component id: og.source.a2_mo_composites.discovery_registry
from __future__ import annotations

__version__ = "0.1.0"

def discovery_registry(self, **kwargs: Any) -> AgentRegistry:
    """/v1/discovery/registry — browse all registered agents. $0.020/call"""
    return self._get_model("/v1/discovery/registry", AgentRegistry, **kwargs)
