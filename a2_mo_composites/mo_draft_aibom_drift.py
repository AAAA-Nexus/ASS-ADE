# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:718
# Component id: mo.source.ass_ade.aibom_drift
from __future__ import annotations

__version__ = "0.1.0"

def aibom_drift(self, model_id: str, **kwargs: Any) -> AibomDriftResult:
    """/v1/aibom/drift — AIBOM lineage verification (AIB-401). $0.040/request"""
    return self._post_model("/v1/aibom/drift", AibomDriftResult, {"model_id": model_id, **kwargs})
