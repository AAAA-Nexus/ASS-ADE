# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:917
# Component id: mo.source.ass_ade.trust_history
from __future__ import annotations

__version__ = "0.1.0"

def trust_history(self, agent_id: str, **kwargs: Any) -> TrustHistory:
    """/v1/trust/history — TCM-101 up to 100 epochs of score trajectory. $0.040/query"""
    return self._post_model("/v1/trust/history", TrustHistory, {"agent_id": agent_id, **kwargs})
