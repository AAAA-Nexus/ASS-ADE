# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:74
# Component id: mo.source.ass_ade.platformmetrics
from __future__ import annotations

__version__ = "0.1.0"

class PlatformMetrics(NexusModel):
    """/v1/metrics"""
    request_volume: int | None = None
    p50_ms: float | None = None
    p99_ms: float | None = None
