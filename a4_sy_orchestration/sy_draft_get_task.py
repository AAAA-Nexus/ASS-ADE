# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:102
# Component id: sy.source.ass_ade.get_task
__version__ = "0.1.0"

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)
