# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_textsummary.py:5
# Component id: mo.source.ass_ade.textsummary
__version__ = "0.1.0"

class TextSummary(NexusModel):
    """/v1/text/summarize"""
    summary: str | None = None
    compression_ratio: float | None = None
    sentences: int | None = None
