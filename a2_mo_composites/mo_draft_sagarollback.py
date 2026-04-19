# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_sagarollback.py:5
# Component id: mo.source.ass_ade.sagarollback
__version__ = "0.1.0"

class SagaRollback(NexusModel):
    """/v1/rollback/saga — RBK-100"""
    saga_id: str | None = None
    steps: list[str] = Field(default_factory=list)
    status: str | None = None
