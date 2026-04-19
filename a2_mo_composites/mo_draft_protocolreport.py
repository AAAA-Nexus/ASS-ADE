# Extracted from C:/!ass-ade/src/ass_ade/protocol/cycle.py:30
# Component id: mo.source.ass_ade.protocolreport
from __future__ import annotations

__version__ = "0.1.0"

class ProtocolReport(BaseModel):
    protocol_name: str = "ASS-ADE Public Enhancement Cycle"
    goal: str
    assessment: ProtocolAssessment
    design_steps: list[str]
    audit: list[ProtocolAuditCheck]
    recommendations: list[str]
    summary: str
