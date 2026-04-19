# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_editplan.py:34
# Component id: at.source.ass_ade.add_delete
__version__ = "0.1.0"

    def add_delete(self, path: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.DELETE,
            path=path,
            description=description or f"Delete {path}",
        ))
        self.validated = False
