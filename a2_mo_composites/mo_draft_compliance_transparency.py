# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1101
# Component id: mo.source.ass_ade.compliance_transparency
from __future__ import annotations

__version__ = "0.1.0"

def compliance_transparency(self, system_id: str, period: str, **kwargs: Any) -> TransparencyReport:
    """/v1/compliance/transparency — quarterly transparency report (TRP-100). $0.080/report"""
    return self._post_model("/v1/compliance/transparency", TransparencyReport, {
        "system_id": system_id, "period": period, **kwargs,
    })
