# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_taskfilter.py:27
# Component id: at.source.ass_ade.find_by_tag
__version__ = "0.1.0"

    def find_by_tag(self, tag: str) -> List[Task]:
        """Find all tasks with a specific tag."""
        all_tasks = self.manager.list_all_tasks()
        return [t for t in all_tasks if tag in t.tags]
