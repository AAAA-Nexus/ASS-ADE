# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_docsresult.py:7
# Component id: mo.source.a2_mo_composites.docsresult
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
