# Extracted from C:/!ass-ade/src/ass_ade/tools/plan.py:29
# Component id: mo.source.ass_ade.editkind
from __future__ import annotations

__version__ = "0.1.0"

class EditKind(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
