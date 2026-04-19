# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1095
# Component id: mo.source.ass_ade.forgebadgeresult
__version__ = "0.1.0"

class ForgeBadgeResult(NexusModel):
    """GET /v1/forge/badge/{id}"""
    badge_id: str | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    issued_at: str | None = None
    valid: bool | None = None
