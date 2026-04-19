# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/lora_flywheel.py:44
# Component id: mo.source.ass_ade.batchresult
__version__ = "0.1.0"

class BatchResult:
    submitted: int
    contribution_id: str | None
    error: str | None = None
    reward_claimed: bool = False
