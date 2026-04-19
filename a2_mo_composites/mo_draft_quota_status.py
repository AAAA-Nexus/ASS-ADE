# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:877
# Component id: mo.source.ass_ade.quota_status
__version__ = "0.1.0"

    def quota_status(self, tree_id: str) -> QuotaStatus:
        """/v1/quota/tree/{id}/status — remaining budget + alerts. $0.020/call"""
        return self._get_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/status", QuotaStatus)
