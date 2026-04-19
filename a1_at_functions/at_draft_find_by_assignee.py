# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskfilter.py:22
# Component id: at.source.ass_ade.find_by_assignee
__version__ = "0.1.0"

    def find_by_assignee(self, assignee: str) -> List[Task]:
        """Find all tasks assigned to a person."""
        all_tasks = self.manager.list_all_tasks()
        return [t for t in all_tasks if t.assignee == assignee]
