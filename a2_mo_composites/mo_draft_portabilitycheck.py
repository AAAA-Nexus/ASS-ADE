# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_portabilitycheck.py:7
# Component id: mo.source.a2_mo_composites.portabilitycheck
from __future__ import annotations

__version__ = "0.1.0"

class PortabilityCheck(NexusModel):
    """/v1/federation/portability — AIF-102"""
    portability_score: float | None = None
    from_platform: str | None = None
    to_platform: str | None = None
    capability_gaps: list[str] = Field(default_factory=list)
