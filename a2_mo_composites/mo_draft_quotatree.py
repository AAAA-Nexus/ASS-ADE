# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:631
# Component id: mo.source.ass_ade.quotatree
from __future__ import annotations

__version__ = "0.1.0"

class QuotaTree(NexusModel):
    """/v1/quota/tree — QTA-100"""
    tree_id: str | None = None
    total_budget: int | None = None
    children: list[dict] = Field(default_factory=list)
