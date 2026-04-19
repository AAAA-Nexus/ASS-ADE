# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bitnetquantizeresponse.py:5
# Component id: mo.source.ass_ade.bitnetquantizeresponse
__version__ = "0.1.0"

class BitNetQuantizeResponse(NexusModel):
    """POST /v1/bitnet/quantize (BIT-104)"""
    quantized_model_id: str | None = None
    original_size_mb: float | None = None
    quantized_size_mb: float | None = None
    compression_ratio: float | None = None
    status: str | None = None
