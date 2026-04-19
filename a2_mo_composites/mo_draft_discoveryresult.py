# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:343
# Component id: mo.source.ass_ade.discoveryresult
from __future__ import annotations

__version__ = "0.1.0"

class DiscoveryResult(NexusModel):
    """/v1/discovery/search and /v1/discovery/recommend"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total: int | None = None
    query: Any = None
