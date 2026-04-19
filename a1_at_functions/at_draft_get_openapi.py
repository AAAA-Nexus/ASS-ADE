# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_openapi.py:7
# Component id: at.source.a1_at_functions.get_openapi
from __future__ import annotations

__version__ = "0.1.0"

def get_openapi(self) -> OpenApiDocument:
    """/openapi.json — free"""
    return self._get_model("/openapi.json", OpenApiDocument)
