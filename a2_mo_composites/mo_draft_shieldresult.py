# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:460
# Component id: mo.source.ass_ade.shieldresult
__version__ = "0.1.0"

class ShieldResult(NexusModel):
    """/v1/security/shield"""
    sanitized: bool | None = None
    blocked: bool | None = None
    payload: dict | None = None
