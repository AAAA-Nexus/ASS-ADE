# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_complianceresult.py:7
# Component id: mo.source.a2_mo_composites.complianceresult
from __future__ import annotations

__version__ = "0.1.0"

class ComplianceResult(NexusModel):
    """/v1/compliance/check and /v1/compliance/eu-ai-act"""
    compliant: bool | None = None
    frameworks: list[str] = Field(default_factory=list)
    certificate_id: str | None = None
    gaps: list[str] = Field(default_factory=list)
