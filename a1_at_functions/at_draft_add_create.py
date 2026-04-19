# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add_create.py:7
# Component id: at.source.a1_at_functions.add_create
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
