# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_bitnetmodel.py:7
# Component id: mo.source.a2_mo_composites.bitnetmodel
from __future__ import annotations

__version__ = "0.1.0"

class BitNetModel(NexusModel):
    """One entry in GET /v1/bitnet/models (BIT-102)"""
    id: str | None = None
    provider: str | None = None
    params_b: float | None = None
    context_length: int | None = None
    memory_gb: float | None = None
    status: str | None = None
