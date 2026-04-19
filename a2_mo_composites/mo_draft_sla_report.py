# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:594
# Component id: mo.source.ass_ade.sla_report
__version__ = "0.1.0"

    def sla_report(self, sla_id: str, metric: str, value: float, **kwargs: Any) -> SlaResult:
        """/v1/sla/report — report SLA metric, auto-detects breaches. $0.020/call"""
        return self._post_model("/v1/sla/report", SlaResult, {"sla_id": sla_id, "metric": metric, "value": value, **kwargs})
