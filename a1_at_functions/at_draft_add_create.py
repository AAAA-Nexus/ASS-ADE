# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_editplan.py:13
# Component id: at.source.ass_ade.add_create
__version__ = "0.1.0"

    def add_create(self, path: str, content: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.CREATE,
            path=path,
            new_string=content,
            description=description or f"Create {path}",
        ))
        self.validated = False
