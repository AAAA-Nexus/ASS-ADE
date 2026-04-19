# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_efficiency_capture.py:7
# Component id: at.source.a1_at_functions.efficiency_capture
from __future__ import annotations

__version__ = "0.1.0"

def efficiency_capture(self, interactions: list[dict], **kwargs: Any) -> EfficiencyResult:
    """/v1/efficiency — ROI signal across agent interactions (PAY-506). $0.040/call"""
    return self._post_model("/v1/efficiency", EfficiencyResult, {"interactions": interactions, **kwargs})
