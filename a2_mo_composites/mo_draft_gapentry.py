# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:36
# Component id: mo.source.ass_ade.gapentry
__version__ = "0.1.0"

class GAPEntry:
    description: str
    ts: float = field(default_factory=time.time)
    source: str = ""
