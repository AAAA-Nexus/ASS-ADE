# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:407
# Component id: mo.source.a2_mo_composites.sla_breach
from __future__ import annotations

__version__ = "0.1.0"

def sla_breach(self, sla_id: str, severity: str, **kwargs: Any) -> SlaResult:
    """/v1/sla/breach — report breach + calculate penalty. $0.040/call"""
    return self._post_model("/v1/sla/breach", SlaResult, {"sla_id": sla_id, "severity": severity, **kwargs})
