# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_bitnetbenchmarkresponse.py:7
# Component id: mo.source.a2_mo_composites.bitnetbenchmarkresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetBenchmarkResponse(NexusModel):
    """POST /v1/bitnet/benchmark (BIT-103)"""
    model: str | None = None
    tokens_per_second: float | None = None
    memory_mb: float | None = None
    latency_ms: float | None = None
    benchmark_id: str | None = None
