# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/a2a/__init__.py:112
# Component id: mo.source.ass_ade.validationissue
__version__ = "0.1.0"

class ValidationIssue:
    """A single validation finding."""

    severity: str  # "error" | "warning" | "info"
    field: str
    message: str
