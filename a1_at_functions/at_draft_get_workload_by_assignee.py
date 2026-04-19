# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskreporter.py:30
# Component id: at.source.ass_ade.get_workload_by_assignee
__version__ = "0.1.0"

    def get_workload_by_assignee(self) -> dict:
        """Count tasks assigned to each person."""
        all_tasks = self.manager.list_all_tasks()
        workload = {}
        for task in all_tasks:
            if task.assignee:
                workload[task.assignee] = workload.get(task.assignee, 0) + 1
        return workload
