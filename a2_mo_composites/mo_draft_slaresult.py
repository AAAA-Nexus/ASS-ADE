# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:324
# Component id: mo.source.ass_ade.slaresult
from __future__ import annotations

__version__ = "0.1.0"

class SlaResult(NexusModel):
    """Generic for report/breach"""
    sla_id: str | None = None
    compliant: bool | None = None
    penalty_usdc: float | None = None
    message: str | None = None
