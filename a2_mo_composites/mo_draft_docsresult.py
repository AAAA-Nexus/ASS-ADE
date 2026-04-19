# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1107
# Component id: mo.source.ass_ade.docsresult
from __future__ import annotations

__version__ = "0.1.0"

class DocsResult(NexusModel):
    ok: bool = False
    path: str | None = None
    files_generated: list[str] = []
    synthesis_applied: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None
