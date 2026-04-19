# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_agentregistry.py:7
# Component id: og.source.a3_og_features.agentregistry
from __future__ import annotations

__version__ = "0.1.0"

class AgentRegistry(NexusModel):
    """/v1/discovery/registry"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total_registered: int | None = None
