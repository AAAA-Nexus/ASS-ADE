# Extracted from C:/!ass-ade/src/ass_ade/tools/plan.py:80
# Component id: at.source.ass_ade.add_delete
from __future__ import annotations

__version__ = "0.1.0"

def add_delete(self, path: str, description: str = "") -> None:
    self.edits.append(PlannedEdit(
        kind=EditKind.DELETE,
        path=path,
        description=description or f"Delete {path}",
    ))
    self.validated = False
