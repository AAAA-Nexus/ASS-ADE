# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:237
# Component id: mo.source.a2_mo_composites.embed
from __future__ import annotations

__version__ = "0.1.0"

def embed(self, values: list[float], **kwargs: Any) -> EmbedResponse:
    """/v1/embed — HELIX compressed embedding. $0.040/request"""
    return self._post_model("/v1/embed", EmbedResponse, {"values": values, **kwargs})
