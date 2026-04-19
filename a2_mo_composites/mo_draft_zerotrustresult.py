# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:253
# Component id: mo.source.ass_ade.zerotrustresult
__version__ = "0.1.0"

class ZeroTrustResult(NexusModel):
    """/v1/auth/zero-trust"""
    allowed: bool | None = None
    trust_level: str | None = None
    reason: str | None = None
