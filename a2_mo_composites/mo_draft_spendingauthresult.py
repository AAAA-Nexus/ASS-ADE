# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_spendingauthresult.py:7
# Component id: mo.source.a2_mo_composites.spendingauthresult
from __future__ import annotations

__version__ = "0.1.0"

class SpendingAuthResult(NexusModel):
    """/v1/spending/authorize — SPG-100"""
    approved: bool | None = None
    approved_amount_usdc: float | None = None
    tau_trust_decay: float | None = None
