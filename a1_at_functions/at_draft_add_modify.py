# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add_modify.py:7
# Component id: at.source.a1_at_functions.add_modify
from __future__ import annotations

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
