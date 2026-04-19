# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:523
# Component id: mo.source.a2_mo_composites.aibom_drift
from __future__ import annotations

__version__ = "0.1.0"

def aibom_drift(self, model_id: str, **kwargs: Any) -> AibomDriftResult:
    """/v1/aibom/drift — AIBOM lineage verification (AIB-401). $0.040/request"""
    return self._post_model("/v1/aibom/drift", AibomDriftResult, {"model_id": model_id, **kwargs})
