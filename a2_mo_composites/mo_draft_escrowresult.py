# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_escrowresult.py:7
# Component id: mo.source.a2_mo_composites.escrowresult
from __future__ import annotations

__version__ = "0.1.0"

class EscrowResult(NexusModel):
    """Generic for release / dispute / arbitrate"""
    escrow_id: str | None = None
    status: str | None = None
    message: str | None = None
