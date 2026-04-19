# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:963
# Component id: mo.source.ass_ade.bitnetinferenceresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetInferenceResponse(NexusModel):
    """POST /v1/bitnet/inference (BIT-100)"""
    result: str | None = None
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    ternary_ops: int | None = None
