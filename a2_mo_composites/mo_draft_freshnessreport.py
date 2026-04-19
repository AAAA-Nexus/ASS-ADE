# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:27
# Component id: mo.source.ass_ade.freshnessreport
__version__ = "0.1.0"

class FreshnessReport:
    path: str
    fresh: bool
    last_read_ts: float | None
    age_hours: float | None
    threshold_hours: float
