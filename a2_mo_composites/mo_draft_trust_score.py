# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:718
# Component id: mo.source.a2_mo_composites.trust_score
from __future__ import annotations

__version__ = "0.1.0"

def trust_score(self, agent_id: str, **kwargs: Any) -> TrustScore:
    """/v1/trust/score — TCM-100 formally bounded score in [0,1]. $0.040/query"""
    return self._post_model("/v1/trust/score", TrustScore, {"agent_id": agent_id, **kwargs})
