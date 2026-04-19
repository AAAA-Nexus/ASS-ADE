# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compliance_transparency.py:7
# Component id: at.source.a1_at_functions.compliance_transparency
from __future__ import annotations

__version__ = "0.1.0"

def compliance_transparency(self, system_id: str, period: str, **kwargs: Any) -> TransparencyReport:
    """/v1/compliance/transparency — quarterly transparency report (TRP-100). $0.080/report"""
    return self._post_model("/v1/compliance/transparency", TransparencyReport, {
        "system_id": system_id, "period": period, **kwargs,
    })
