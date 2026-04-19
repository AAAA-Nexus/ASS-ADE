# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:40
# Component id: mo.source.ass_ade.openapidocument
from __future__ import annotations

__version__ = "0.1.0"

class OpenApiDocument(NexusModel):
    openapi: str | None = None
    info: OpenApiInfo
