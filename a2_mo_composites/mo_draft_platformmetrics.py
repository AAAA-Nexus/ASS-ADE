# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_platformmetrics.py:5
# Component id: mo.source.ass_ade.platformmetrics
__version__ = "0.1.0"

class PlatformMetrics(NexusModel):
    """/v1/metrics"""
    request_volume: int | None = None
    p50_ms: float | None = None
    p99_ms: float | None = None
