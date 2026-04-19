# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_formatconversion.py:7
# Component id: at.source.a1_at_functions.formatconversion
from __future__ import annotations

__version__ = "0.1.0"

class FormatConversion(NexusModel):
    """/v1/data/format-convert"""
    result: str | None = None
    from_format: str | None = None
    to_format: str | None = None
