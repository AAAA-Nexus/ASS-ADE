# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_quotatree.py:5
# Component id: mo.source.ass_ade.quotatree
__version__ = "0.1.0"

class QuotaTree(NexusModel):
    """/v1/quota/tree — QTA-100"""
    tree_id: str | None = None
    total_budget: int | None = None
    children: list[dict] = Field(default_factory=list)
