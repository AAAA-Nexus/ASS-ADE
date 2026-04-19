# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:297
# Component id: mo.source.ass_ade.get_metrics
__version__ = "0.1.0"

    def get_metrics(self) -> PlatformMetrics:
        """/v1/metrics — aggregated public telemetry, free"""
        return self._get_model("/v1/metrics", PlatformMetrics)
