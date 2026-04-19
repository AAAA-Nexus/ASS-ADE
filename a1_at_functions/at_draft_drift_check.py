# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_drift_check.py:7
# Component id: at.source.a1_at_functions.drift_check
from __future__ import annotations

__version__ = "0.1.0"

def drift_check(
    self,
    model_id: str,
    reference_data: dict | None = None,
    current_data: dict | None = None,
    **kwargs: Any,
) -> DriftCheck:
    """/v1/drift/check — PSI drift detection ≤0.20 (DRG-100). $0.010/check"""
    return self._post_model("/v1/drift/check", DriftCheck, {
        "model_id": model_id,
        "reference_data": reference_data or {},
        "current_data": current_data or {},
        **kwargs,
    })
