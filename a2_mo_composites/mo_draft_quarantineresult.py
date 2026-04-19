# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_quarantineresult.py:5
# Component id: mo.source.ass_ade.quarantineresult
__version__ = "0.1.0"

class QuarantineResult(NexusModel):
    """/v1/agent/quarantine"""
    quarantined: bool | None = None
    agent_id: str | None = None
    reason: str | None = None
