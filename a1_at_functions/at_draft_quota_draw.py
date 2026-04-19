# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_quota_draw.py:7
# Component id: at.source.a1_at_functions.quota_draw
from __future__ import annotations

__version__ = "0.1.0"

def quota_draw(self, tree_id: str, child_id: str, tokens: int, idempotency_key: str, **kwargs: Any) -> QuotaDrawResult:
    """/v1/quota/tree/{id}/draw — deduct tokens with idempotency. $0.020/call"""
    return self._post_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/draw", QuotaDrawResult, {
        "child_id": child_id, "tokens": tokens, "idempotency_key": idempotency_key, **kwargs,
    })
