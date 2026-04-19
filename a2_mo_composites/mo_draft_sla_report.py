# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:399
# Component id: mo.source.a2_mo_composites.sla_report
from __future__ import annotations

__version__ = "0.1.0"

def sla_report(self, sla_id: str, metric: str, value: float, **kwargs: Any) -> SlaResult:
    """/v1/sla/report — report SLA metric, auto-detects breaches. $0.020/call"""
    return self._post_model("/v1/sla/report", SlaResult, {"sla_id": sla_id, "metric": metric, "value": value, **kwargs})
