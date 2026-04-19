# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_taskmanager.py:21
# Component id: mo.source.ass_ade.get_task
__version__ = "0.1.0"

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)
