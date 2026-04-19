# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_embedresponse.py:7
# Component id: mo.source.a2_mo_composites.embedresponse
from __future__ import annotations

__version__ = "0.1.0"

class EmbedResponse(NexusModel):
    """/v1/embed — HELIX compressed embedding"""
    embedding: list[float] | None = Field(default=None)
    compressed: str | None = None    # base64 HELIX blob
    dimensions: int | None = None
    latency_ms: float | None = None
