# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add_delete.py:7
# Component id: at.source.a1_at_functions.add_delete
from __future__ import annotations

__version__ = "0.1.0"

def add_delete(self, path: str, description: str = "") -> None:
    self.edits.append(PlannedEdit(
        kind=EditKind.DELETE,
        path=path,
        description=description or f"Delete {path}",
    ))
    self.validated = False
