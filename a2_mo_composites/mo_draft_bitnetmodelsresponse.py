# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_bitnetmodelsresponse.py:7
# Component id: mo.source.a2_mo_composites.bitnetmodelsresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetModelsResponse(NexusModel):
    """GET /v1/bitnet/models"""
    models: list[BitNetModel] = Field(default_factory=list)
    count: int | None = None
