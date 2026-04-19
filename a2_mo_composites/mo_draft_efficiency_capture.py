# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:982
# Component id: mo.source.a2_mo_composites.efficiency_capture
from __future__ import annotations

__version__ = "0.1.0"

def efficiency_capture(self, interactions: list[dict], **kwargs: Any) -> EfficiencyResult:
    """/v1/efficiency — ROI signal across agent interactions (PAY-506). $0.040/call"""
    return self._post_model("/v1/efficiency", EfficiencyResult, {"interactions": interactions, **kwargs})
