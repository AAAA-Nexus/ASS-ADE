# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_aibom_drift.py:7
# Component id: at.source.a1_at_functions.aibom_drift
from __future__ import annotations

__version__ = "0.1.0"

def aibom_drift(self, model_id: str, **kwargs: Any) -> AibomDriftResult:
    """/v1/aibom/drift — AIBOM lineage verification (AIB-401). $0.040/request"""
    return self._post_model("/v1/aibom/drift", AibomDriftResult, {"model_id": model_id, **kwargs})
