# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:489
# Component id: mo.source.ass_ade.auditlogentry
__version__ = "0.1.0"

class AuditLogEntry(NexusModel):
    """/v1/audit/log"""
    entry_id: str | None = None
    hash: str | None = None
    timestamp: Any = None
