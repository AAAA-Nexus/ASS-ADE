# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_quotadrawresult.py:5
# Component id: mo.source.ass_ade.quotadrawresult
__version__ = "0.1.0"

class QuotaDrawResult(NexusModel):
    """/v1/quota/tree/{id}/draw — QTA-100"""
    drawn: int | None = None
    remaining: int | None = None
    idempotency_key: str | None = None
