# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:496
# Component id: mo.source.ass_ade.auditverifyresult
__version__ = "0.1.0"

class AuditVerifyResult(NexusModel):
    """/v1/audit/verify"""
    intact: bool | None = None
    chain_length: int | None = None
    first_entry: str | None = None
    last_entry: str | None = None
