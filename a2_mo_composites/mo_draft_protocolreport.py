# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/cycle.py:30
# Component id: mo.source.ass_ade.protocolreport
__version__ = "0.1.0"

class ProtocolReport(BaseModel):
    protocol_name: str = "ASS-ADE Public Enhancement Cycle"
    goal: str
    assessment: ProtocolAssessment
    design_steps: list[str]
    audit: list[ProtocolAuditCheck]
    recommendations: list[str]
    summary: str
