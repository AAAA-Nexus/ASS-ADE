# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:907
# Component id: mo.source.ass_ade.thinkroute
from __future__ import annotations

__version__ = "0.1.0"

class ThinkRoute(NexusModel):
    """/v1/routing/think — POP-1207"""
    complexity: Any = None   # "low" | "medium" | "high"
    recommended_tier: str | None = None
    recommended_model: str | None = None
