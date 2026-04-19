# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_incidentreport.py:7
# Component id: mo.source.a2_mo_composites.incidentreport
from __future__ import annotations

__version__ = "0.1.0"

class IncidentReport(NexusModel):
    """/v1/compliance/incident — INC-100"""
    incident_id: str | None = None
    severity: str | None = None
    notification_deadline: str | None = None
