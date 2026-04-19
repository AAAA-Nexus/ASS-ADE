# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_task.py:5
# Component id: mo.source.ass_ade.task
__version__ = "0.1.0"

class Task:
    """Task data structure."""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)
