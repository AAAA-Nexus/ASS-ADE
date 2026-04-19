# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_slaresult.py:7
# Component id: mo.source.a2_mo_composites.slaresult
from __future__ import annotations

__version__ = "0.1.0"

class SlaResult(NexusModel):
    """Generic for report/breach"""
    sla_id: str | None = None
    compliant: bool | None = None
    penalty_usdc: float | None = None
    message: str | None = None
