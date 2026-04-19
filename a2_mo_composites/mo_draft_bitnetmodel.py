# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bitnetmodel.py:5
# Component id: mo.source.ass_ade.bitnetmodel
__version__ = "0.1.0"

class BitNetModel(NexusModel):
    """One entry in GET /v1/bitnet/models (BIT-102)"""
    id: str | None = None
    provider: str | None = None
    params_b: float | None = None
    context_length: int | None = None
    memory_gb: float | None = None
    status: str | None = None
