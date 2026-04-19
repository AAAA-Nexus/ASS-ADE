# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_bitnetinferenceresponse.py:7
# Component id: mo.source.a2_mo_composites.bitnetinferenceresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetInferenceResponse(NexusModel):
    """POST /v1/bitnet/inference (BIT-100)"""
    result: str | None = None
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    ternary_ops: int | None = None
