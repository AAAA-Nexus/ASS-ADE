# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:297
# Component id: mo.source.ass_ade.get_metrics
from __future__ import annotations

__version__ = "0.1.0"

def get_metrics(self) -> PlatformMetrics:
    """/v1/metrics — aggregated public telemetry, free"""
    return self._get_model("/v1/metrics", PlatformMetrics)
