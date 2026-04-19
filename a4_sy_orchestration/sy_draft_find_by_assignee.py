# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/examples/02-rebuild-a-codebase/sample_project/main.py:164
# Component id: sy.source.ass_ade.find_by_assignee
__version__ = "0.1.0"

    def find_by_assignee(self, assignee: str) -> List[Task]:
        """Find all tasks assigned to a person."""
        all_tasks = self.manager.list_all_tasks()
        return [t for t in all_tasks if t.assignee == assignee]
