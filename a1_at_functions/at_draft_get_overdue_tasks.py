# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskfilter.py:17
# Component id: at.source.ass_ade.get_overdue_tasks
__version__ = "0.1.0"

    def get_overdue_tasks(self) -> List[Task]:
        """Get all non-done tasks (would check dates in real impl)."""
        all_tasks = self.manager.list_all_tasks()
        return filter_tasks_by_status(all_tasks, TaskStatus.TODO)
