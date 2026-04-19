# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1080
# Component id: mo.source.ass_ade.compliance_incident
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
