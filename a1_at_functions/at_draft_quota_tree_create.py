# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_quota_tree_create.py:7
# Component id: at.source.a1_at_functions.quota_tree_create
from __future__ import annotations

__version__ = "0.1.0"

def quota_tree_create(self, total_budget: int, children: list[str], **kwargs: Any) -> QuotaTree:
    """/v1/quota/tree — create budget tree (QME-100). $0.040/call"""
    return self._post_model("/v1/quota/tree", QuotaTree, {"total_budget": total_budget, "children": children, **kwargs})
