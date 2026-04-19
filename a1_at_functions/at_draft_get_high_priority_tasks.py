# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskfilter.py:12
# Component id: at.source.ass_ade.get_high_priority_tasks
__version__ = "0.1.0"

    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high-priority and urgent tasks."""
        all_tasks = self.manager.list_all_tasks()
        return filter_tasks_by_priority(all_tasks, TaskPriority.HIGH)
