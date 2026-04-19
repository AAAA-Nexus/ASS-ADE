# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:871
# Component id: mo.source.ass_ade.quota_draw
__version__ = "0.1.0"

    def quota_draw(self, tree_id: str, child_id: str, tokens: int, idempotency_key: str, **kwargs: Any) -> QuotaDrawResult:
        """/v1/quota/tree/{id}/draw — deduct tokens with idempotency. $0.020/call"""
        return self._post_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/draw", QuotaDrawResult, {
            "child_id": child_id, "tokens": tokens, "idempotency_key": idempotency_key, **kwargs,
        })
