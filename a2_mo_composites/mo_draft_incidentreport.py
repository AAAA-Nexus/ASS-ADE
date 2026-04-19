# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_incidentreport.py:5
# Component id: mo.source.ass_ade.incidentreport
__version__ = "0.1.0"

class IncidentReport(NexusModel):
    """/v1/compliance/incident — INC-100"""
    incident_id: str | None = None
    severity: str | None = None
    notification_deadline: str | None = None
