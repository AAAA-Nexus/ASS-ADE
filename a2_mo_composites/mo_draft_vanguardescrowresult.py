# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1027
# Component id: mo.source.ass_ade.vanguardescrowresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardEscrowResult(NexusModel):
    """POST /v1/vanguard/escrow/lock-and-verify"""
    lock_id: str | None = None
    verified: bool | None = None
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
