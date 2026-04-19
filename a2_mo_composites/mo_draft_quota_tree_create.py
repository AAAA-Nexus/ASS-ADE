# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:867
# Component id: mo.source.ass_ade.quota_tree_create
__version__ = "0.1.0"

    def quota_tree_create(self, total_budget: int, children: list[str], **kwargs: Any) -> QuotaTree:
        """/v1/quota/tree — create budget tree (QME-100). $0.040/call"""
        return self._post_model("/v1/quota/tree", QuotaTree, {"total_budget": total_budget, "children": children, **kwargs})
