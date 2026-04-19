# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_toolref.py:5
# Component id: mo.source.ass_ade.toolref
__version__ = "0.1.0"

class ToolRef:
    name: str
    score: float
    server: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
