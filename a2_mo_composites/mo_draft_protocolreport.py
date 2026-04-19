# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_protocolreport.py:7
# Component id: mo.source.a2_mo_composites.protocolreport
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
