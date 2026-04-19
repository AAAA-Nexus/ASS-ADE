# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:93
# Component id: sy.source.ass_ade.add_task
__version__ = "0.1.0"

    def add_task(self, task: Task) -> bool:
        """Add a task to the collection."""
        if not validate_task_id(task.id):
            return False
        if not validate_task_title(task.title):
            return False
        self.tasks[task.id] = task
        return True
