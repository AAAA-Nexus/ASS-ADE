# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_inferenceresponse.py:7
# Component id: mo.source.a2_mo_composites.inferenceresponse
from __future__ import annotations

__version__ = "0.1.0"

class InferenceResponse(NexusModel):
    """/v1/inference and /v1/embed"""
    result: str | None = None
    text: str | None = None          # alias used by some versions
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    helix_metadata: dict | None = None
