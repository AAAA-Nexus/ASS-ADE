# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:246
# Component id: mo.source.ass_ade.sybilcheckresult
__version__ = "0.1.0"

class SybilCheckResult(NexusModel):
    """/v1/identity/sybil-check"""
    sybil_risk: str | None = None   # "low" | "medium" | "high"
    score: float | None = None
    flags: list[str] = Field(default_factory=list)
