# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:957
# Component id: mo.source.ass_ade.bitnetmodelsresponse
from __future__ import annotations

__version__ = "0.1.0"

class BitNetModelsResponse(NexusModel):
    """GET /v1/bitnet/models"""
    models: list[BitNetModel] = Field(default_factory=list)
    count: int | None = None
