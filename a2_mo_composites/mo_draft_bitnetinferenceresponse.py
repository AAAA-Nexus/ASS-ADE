# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bitnetinferenceresponse.py:5
# Component id: mo.source.ass_ade.bitnetinferenceresponse
__version__ = "0.1.0"

class BitNetInferenceResponse(NexusModel):
    """POST /v1/bitnet/inference (BIT-100)"""
    result: str | None = None
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    ternary_ops: int | None = None
