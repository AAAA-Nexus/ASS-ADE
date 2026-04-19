# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:503
# Component id: mo.source.a2_mo_composites.threat_score
from __future__ import annotations

__version__ = "0.1.0"

def threat_score(self, payload: dict, **kwargs: Any) -> ThreatScore:
    """/v1/threat/score — multi-vector threat scoring (SEC-303). $0.040/request"""
    return self._post_model("/v1/threat/score", ThreatScore, {"payload": payload, **kwargs})
