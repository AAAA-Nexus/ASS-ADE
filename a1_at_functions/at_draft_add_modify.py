# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_editplan.py:22
# Component id: at.source.ass_ade.add_modify
__version__ = "0.1.0"

    def add_modify(
        self, path: str, old_string: str, new_string: str, description: str = ""
    ) -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.MODIFY,
            path=path,
            old_string=old_string,
            new_string=new_string,
            description=description or f"Edit {path}",
        ))
        self.validated = False
