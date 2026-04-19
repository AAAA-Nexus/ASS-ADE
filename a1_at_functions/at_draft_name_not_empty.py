# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:102
# Component id: at.source.ass_ade.name_not_empty
from __future__ import annotations

__version__ = "0.1.0"

def name_not_empty(cls, v: str) -> str:
    if not v.strip():
        raise ValueError("Agent card name must not be empty")
    return v
