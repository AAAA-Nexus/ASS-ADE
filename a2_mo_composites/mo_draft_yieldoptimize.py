# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_yieldoptimize.py:7
# Component id: mo.source.a2_mo_composites.yieldoptimize
from __future__ import annotations

__version__ = "0.1.0"

class YieldOptimize(NexusModel):
    """/v1/defi/yield-optimize — YLD-100"""
    allocations: list[dict] = Field(default_factory=list)
    expected_apy: float | None = None
    alpha_above_baseline: float | None = None
