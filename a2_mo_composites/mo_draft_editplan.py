# Extracted from C:/!ass-ade/src/ass_ade/tools/plan.py:51
# Component id: mo.source.ass_ade.editplan
from __future__ import annotations

__version__ = "0.1.0"

class EditPlan:
    """A batch of file operations to apply atomically."""

    edits: list[PlannedEdit] = field(default_factory=list)
    description: str = ""
    validated: bool = False
    applied: bool = False

    def add_create(self, path: str, content: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.CREATE,
            path=path,
            new_string=content,
            description=description or f"Create {path}",
        ))
        self.validated = False

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

    def add_delete(self, path: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.DELETE,
            path=path,
            description=description or f"Delete {path}",
        ))
        self.validated = False
