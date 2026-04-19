# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:106
# Component id: sy.source.ass_ade.update_task_status
__version__ = "0.1.0"

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
        """Update a task's status."""
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            return True
        return False
