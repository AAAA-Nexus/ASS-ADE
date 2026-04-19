# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_formatconversion.py:5
# Component id: at.source.ass_ade.formatconversion
__version__ = "0.1.0"

class FormatConversion(NexusModel):
    """/v1/data/format-convert"""
    result: str | None = None
    from_format: str | None = None
    to_format: str | None = None
