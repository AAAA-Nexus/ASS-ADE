# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:519
# Component id: mo.source.a2_mo_composites.compliance_eu_ai_act
from __future__ import annotations

__version__ = "0.1.0"

def compliance_eu_ai_act(self, system_description: str, **kwargs: Any) -> ComplianceResult:
    """/v1/compliance/eu-ai-act — Annex IV conformity certificate. $0.040/check"""
    return self._post_model("/v1/compliance/eu-ai-act", ComplianceResult, {"system_description": system_description, **kwargs})
