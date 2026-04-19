# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/cycle.py:13
# Component id: mo.source.ass_ade.protocolauditcheck
__version__ = "0.1.0"

class ProtocolAuditCheck(BaseModel):
    name: str
    passed: bool
    detail: str
