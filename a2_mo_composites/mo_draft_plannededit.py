# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_plannededit.py:7
# Component id: mo.source.a2_mo_composites.plannededit
from __future__ import annotations

__version__ = "0.1.0"

class PlannedEdit:
    """A single file operation within an edit plan."""

    kind: EditKind
    path: str  # relative to working dir
    old_string: str = ""  # for MODIFY
    new_string: str = ""  # for MODIFY and CREATE
    description: str = ""
    diff: str = ""  # populated during validation

    # Internal state
    _original_content: str | None = None
