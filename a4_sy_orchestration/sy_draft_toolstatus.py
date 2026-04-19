# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/system.py:9
# Component id: sy.source.ass_ade.toolstatus
__version__ = "0.1.0"

class ToolStatus:
    name: str
    available: bool
    version: str | None = None
    error: str | None = None
