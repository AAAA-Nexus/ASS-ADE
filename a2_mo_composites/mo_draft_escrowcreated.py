# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_escrowcreated.py:7
# Component id: mo.source.a2_mo_composites.escrowcreated
from __future__ import annotations

__version__ = "0.1.0"

class EscrowCreated(NexusModel):
    """/v1/escrow/create"""
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
    release_conditions: list[str] = Field(default_factory=list)
    expires_at: str | None = None
