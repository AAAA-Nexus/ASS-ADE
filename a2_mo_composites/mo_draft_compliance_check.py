# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:710
# Component id: mo.source.ass_ade.compliance_check
from __future__ import annotations

__version__ = "0.1.0"

def compliance_check(self, system_description: str, **kwargs: Any) -> ComplianceResult:
    """/v1/compliance/check — EU AI Act / NIST AI RMF / ISO 42001 (CMP-100). $0.040/check"""
    return self._post_model("/v1/compliance/check", ComplianceResult, {"system_description": system_description, **kwargs})
