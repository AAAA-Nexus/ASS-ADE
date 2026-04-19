# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/plan.py:36
# Component id: mo.source.ass_ade.plannededit
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
