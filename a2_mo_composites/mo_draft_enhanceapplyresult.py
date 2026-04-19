# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1170
# Component id: mo.source.ass_ade.enhanceapplyresult
__version__ = "0.1.0"

class EnhanceApplyResult(NexusModel):
    ok: bool = False
    path: str | None = None
    applied_count: int = 0
    blueprints: list[dict[str, Any]] = []
    rebuild_triggered: bool = False
    certified: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None
