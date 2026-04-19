# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_liquidationcheck.py:7
# Component id: mo.source.a2_mo_composites.liquidationcheck
from __future__ import annotations

__version__ = "0.1.0"

class LiquidationCheck(NexusModel):
    """/v1/defi/liquidation-check — LQS-100"""
    health_factor: float | None = None
    time_to_liquidation_s: int | None = None
    recommended_top_up_usdc: float | None = None
