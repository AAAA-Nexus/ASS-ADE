# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskreporter.py:22
# Component id: at.source.ass_ade.get_priority_distribution
__version__ = "0.1.0"

    def get_priority_distribution(self) -> dict:
        """Get count of tasks by priority."""
        all_tasks = self.manager.list_all_tasks()
        distribution = {p: 0 for p in TaskPriority}
        for task in all_tasks:
            distribution[task.priority] += 1
        return distribution
