# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_vanguardescrowresult.py:7
# Component id: mo.source.a2_mo_composites.vanguardescrowresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardEscrowResult(NexusModel):
    """POST /v1/vanguard/escrow/lock-and-verify"""
    lock_id: str | None = None
    verified: bool | None = None
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
