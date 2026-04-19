# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/plan.py:29
# Component id: mo.source.ass_ade.editkind
__version__ = "0.1.0"

class EditKind(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
