# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memorytrimresult.py:5
# Component id: mo.source.ass_ade.memorytrimresult
__version__ = "0.1.0"

class MemoryTrimResult(NexusModel):
    """/v1/memory/trim — INF-815"""
    tokens_before: int | None = None
    tokens_after: int | None = None
    pruned_entries: int | None = None
