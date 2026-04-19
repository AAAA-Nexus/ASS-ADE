# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_toolstatus.py:5
# Component id: mo.source.ass_ade.toolstatus
__version__ = "0.1.0"

class ToolStatus:
    name: str
    available: bool
    version: str | None = None
    error: str | None = None
