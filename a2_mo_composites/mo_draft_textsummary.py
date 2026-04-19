# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:831
# Component id: mo.source.ass_ade.textsummary
from __future__ import annotations

__version__ = "0.1.0"

class TextSummary(NexusModel):
    """/v1/text/summarize"""
    summary: str | None = None
    compression_ratio: float | None = None
    sentences: int | None = None
