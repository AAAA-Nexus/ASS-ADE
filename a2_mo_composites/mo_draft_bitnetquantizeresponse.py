# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:981
# Component id: mo.source.ass_ade.bitnetquantizeresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetQuantizeResponse(NexusModel):
    """POST /v1/bitnet/quantize (BIT-104)"""
    quantized_model_id: str | None = None
    original_size_mb: float | None = None
    quantized_size_mb: float | None = None
    compression_ratio: float | None = None
    status: str | None = None
