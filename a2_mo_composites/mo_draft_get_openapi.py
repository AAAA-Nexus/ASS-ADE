# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:277
# Component id: mo.source.ass_ade.get_openapi
from __future__ import annotations

__version__ = "0.1.0"

def get_openapi(self) -> OpenApiDocument:
    """/openapi.json — free"""
    return self._get_model("/openapi.json", OpenApiDocument)
