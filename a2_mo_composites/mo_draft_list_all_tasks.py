# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_taskmanager.py:40
# Component id: mo.source.ass_ade.list_all_tasks
__version__ = "0.1.0"

    def list_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())
