# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:698
# Component id: mo.source.ass_ade.threat_score
from __future__ import annotations

__version__ = "0.1.0"

def threat_score(self, payload: dict, **kwargs: Any) -> ThreatScore:
    """/v1/threat/score — multi-vector threat scoring (SEC-303). $0.040/request"""
    return self._post_model("/v1/threat/score", ThreatScore, {"payload": payload, **kwargs})
