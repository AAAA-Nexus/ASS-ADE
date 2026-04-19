# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_costattribution.py:7
# Component id: mo.source.a2_mo_composites.costattribution
from __future__ import annotations

__version__ = "0.1.0"

class CostAttribution(NexusModel):
    """/v1/costs/attribute — DEV-603"""
    total_tokens: int | None = None
    by_agent: dict | None = None
    by_task: dict | None = None
    by_model: dict | None = None
