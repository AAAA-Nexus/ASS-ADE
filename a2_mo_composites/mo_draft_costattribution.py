# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:892
# Component id: mo.source.ass_ade.costattribution
from __future__ import annotations

__version__ = "0.1.0"

class CostAttribution(NexusModel):
    """/v1/costs/attribute — DEV-603"""
    total_tokens: int | None = None
    by_agent: dict | None = None
    by_task: dict | None = None
    by_model: dict | None = None
