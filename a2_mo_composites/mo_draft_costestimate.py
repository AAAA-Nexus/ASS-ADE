# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_costestimate.py:7
# Component id: mo.source.a2_mo_composites.costestimate
from __future__ import annotations

__version__ = "0.1.0"

class CostEstimate(NexusModel):
    currency: str = "USDC"
    unit_cost: float | None = None
    rate_limit_rpm: int | None = None
    rate_limit_tpm: int | None = None
    notes: str | None = None
