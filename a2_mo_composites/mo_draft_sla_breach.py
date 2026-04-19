# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:602
# Component id: mo.source.ass_ade.sla_breach
__version__ = "0.1.0"

    def sla_breach(self, sla_id: str, severity: str, **kwargs: Any) -> SlaResult:
        """/v1/sla/breach — report breach + calculate penalty. $0.040/call"""
        return self._post_model("/v1/sla/breach", SlaResult, {"sla_id": sla_id, "severity": severity, **kwargs})
