# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_discoveryresult.py:7
# Component id: mo.source.a2_mo_composites.discoveryresult
from __future__ import annotations

__version__ = "0.1.0"

class DiscoveryResult(NexusModel):
    """/v1/discovery/search and /v1/discovery/recommend"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total: int | None = None
    query: Any = None
