# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_thinkroute.py:7
# Component id: mo.source.a2_mo_composites.thinkroute
from __future__ import annotations

__version__ = "0.1.0"

class ThinkRoute(NexusModel):
    """/v1/routing/think — POP-1207"""
    complexity: Any = None   # "low" | "medium" | "high"
    recommended_tier: str | None = None
    recommended_model: str | None = None
