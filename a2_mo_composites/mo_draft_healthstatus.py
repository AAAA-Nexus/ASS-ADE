# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:28
# Component id: mo.source.ass_ade.healthstatus
__version__ = "0.1.0"

class HealthStatus(NexusModel):
    status: str
    version: str | None = None
    build: str | None = None
    epoch: int | None = None
