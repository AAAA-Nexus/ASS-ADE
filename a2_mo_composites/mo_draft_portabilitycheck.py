# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:604
# Component id: mo.source.ass_ade.portabilitycheck
from __future__ import annotations

__version__ = "0.1.0"

class PortabilityCheck(NexusModel):
    """/v1/federation/portability — AIF-102"""
    portability_score: float | None = None
    from_platform: str | None = None
    to_platform: str | None = None
    capability_gaps: list[str] = Field(default_factory=list)
