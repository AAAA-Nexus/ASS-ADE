# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/bas.py:16
# Component id: mo.source.ass_ade.alert
__version__ = "0.1.0"

class Alert:
    kind: str
    severity: str
    payload: dict
    ts: str
    cooldown_skipped: bool = False
