# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_quotatree.py:7
# Component id: mo.source.a2_mo_composites.quotatree
from __future__ import annotations

__version__ = "0.1.0"

class QuotaTree(NexusModel):
    """/v1/quota/tree — QTA-100"""
    tree_id: str | None = None
    total_budget: int | None = None
    children: list[dict] = Field(default_factory=list)
