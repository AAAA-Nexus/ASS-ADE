# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_taskmanager.py:12
# Component id: mo.source.ass_ade.add_task
__version__ = "0.1.0"

    def add_task(self, task: Task) -> bool:
        """Add a task to the collection."""
        if not validate_task_id(task.id):
            return False
        if not validate_task_title(task.title):
            return False
        self.tasks[task.id] = task
        return True
