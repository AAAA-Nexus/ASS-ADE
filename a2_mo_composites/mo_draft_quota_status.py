# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:682
# Component id: mo.source.a2_mo_composites.quota_status
from __future__ import annotations

__version__ = "0.1.0"

def quota_status(self, tree_id: str) -> QuotaStatus:
    """/v1/quota/tree/{id}/status — remaining budget + alerts. $0.020/call"""
    return self._get_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/status", QuotaStatus)
