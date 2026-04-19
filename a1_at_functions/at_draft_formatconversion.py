# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:860
# Component id: at.source.ass_ade.formatconversion
from __future__ import annotations

__version__ = "0.1.0"

class FormatConversion(NexusModel):
    """/v1/data/format-convert"""
    result: str | None = None
    from_format: str | None = None
    to_format: str | None = None
