# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_contextpacket.py:7
# Component id: mo.source.a2_mo_composites.contextpacket
from __future__ import annotations

__version__ = "0.1.0"

class ContextPacket(BaseModel):
    task_description: str
    recon_verdict: str
    source_urls: list[str] = Field(default_factory=list)
    files: list[ContextFile] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
