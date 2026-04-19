# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_discoveredagent.py:7
# Component id: mo.source.a2_mo_composites.discoveredagent
from __future__ import annotations

__version__ = "0.1.0"

class DiscoveredAgent(NexusModel):
    agent_id: Any = None
    name: str | None = None
    capabilities: Any = None
    reputation_score: float | None = None
    endpoint: str | None = None
    match_score: float | None = None
