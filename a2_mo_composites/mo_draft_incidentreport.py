# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:799
# Component id: mo.source.ass_ade.incidentreport
from __future__ import annotations

__version__ = "0.1.0"

class IncidentReport(NexusModel):
    """/v1/compliance/incident — INC-100"""
    incident_id: str | None = None
    severity: str | None = None
    notification_deadline: str | None = None
