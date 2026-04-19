# Extracted from C:/!ass-ade/src/ass_ade/tools/plan.py:59
# Component id: at.source.ass_ade.add_create
from __future__ import annotations

__version__ = "0.1.0"

def add_create(self, path: str, content: str, description: str = "") -> None:
    self.edits.append(PlannedEdit(
        kind=EditKind.CREATE,
        path=path,
        new_string=content,
        description=description or f"Create {path}",
    ))
    self.validated = False
