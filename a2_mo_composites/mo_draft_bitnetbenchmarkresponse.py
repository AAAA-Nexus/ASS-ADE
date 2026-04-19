# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bitnetbenchmarkresponse.py:5
# Component id: mo.source.ass_ade.bitnetbenchmarkresponse
__version__ = "0.1.0"

class BitNetBenchmarkResponse(NexusModel):
    """POST /v1/bitnet/benchmark (BIT-103)"""
    model: str | None = None
    tokens_per_second: float | None = None
    memory_mb: float | None = None
    latency_ms: float | None = None
    benchmark_id: str | None = None
