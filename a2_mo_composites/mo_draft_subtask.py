# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_subtask.py:5
# Component id: mo.source.ass_ade.subtask
__version__ = "0.1.0"

class SubTask:
    id: str
    description: str
    priority: float
    deps: list[str] = field(default_factory=list)
