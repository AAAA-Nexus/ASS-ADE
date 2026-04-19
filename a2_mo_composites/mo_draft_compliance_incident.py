# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:885
# Component id: mo.source.a2_mo_composites.compliance_incident
from __future__ import annotations

__version__ = "0.1.0"

def compliance_incident(
    self,
    system_id: str | None = None,
    description: str | None = None,
    severity: str | None = None,
    *,
    incident_id: str | None = None,
    **kwargs: Any,
) -> IncidentReport:
    """/v1/compliance/incident — EU AI Act Art.73 incident report (INC-100). $0.020/report"""
    return self._post_model("/v1/compliance/incident", IncidentReport, {
        "system_id": system_id or incident_id or "",
        "description": description or "CLI incident report",
        "severity": severity or "medium",
        **kwargs,
    })
