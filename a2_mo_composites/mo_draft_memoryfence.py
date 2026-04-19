# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memoryfence.py:5
# Component id: mo.source.ass_ade.memoryfence
__version__ = "0.1.0"

class MemoryFence(NexusModel):
    """/v1/memory/fence — MFN-100"""
    fence_id: str | None = None
    namespace: str | None = None
    hmac_key_set: bool | None = None
