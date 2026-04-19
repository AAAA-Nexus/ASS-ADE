# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_metrics.py:7
# Component id: at.source.a1_at_functions.get_metrics
from __future__ import annotations

__version__ = "0.1.0"

def get_metrics(self) -> PlatformMetrics:
    """/v1/metrics — aggregated public telemetry, free"""
    return self._get_model("/v1/metrics", PlatformMetrics)
