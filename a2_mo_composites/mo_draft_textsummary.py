# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_textsummary.py:7
# Component id: mo.source.a2_mo_composites.textsummary
from __future__ import annotations

__version__ = "0.1.0"

class TextSummary(NexusModel):
    """/v1/text/summarize"""
    summary: str | None = None
    compression_ratio: float | None = None
    sentences: int | None = None
