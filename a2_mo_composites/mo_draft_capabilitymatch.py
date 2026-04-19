# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_capabilitymatch.py:7
# Component id: mo.source.a2_mo_composites.capabilitymatch
from __future__ import annotations

__version__ = "0.1.0"

class CapabilityMatch(NexusModel):
    """/v1/agents/capabilities/match"""
    matches: list[DiscoveredAgent] = Field(default_factory=list)
    task: str | None = None
