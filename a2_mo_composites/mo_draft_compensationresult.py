# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_compensationresult.py:5
# Component id: mo.source.ass_ade.compensationresult
__version__ = "0.1.0"

class CompensationResult(NexusModel):
    """/v1/rollback/saga/{id}/compensate — RBK-100"""
    saga_id: str | None = None
    compensated_steps: list[str] = Field(default_factory=list)
    success: bool | None = None
