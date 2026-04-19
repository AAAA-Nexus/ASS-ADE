# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_taskmanager.py:25
# Component id: mo.source.ass_ade.update_task_status
__version__ = "0.1.0"

    def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
        """Update a task's status."""
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            return True
        return False
