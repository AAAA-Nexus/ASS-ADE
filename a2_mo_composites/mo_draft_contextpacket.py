# Extracted from C:/!ass-ade/src/ass_ade/context_memory.py:37
# Component id: mo.source.ass_ade.contextpacket
from __future__ import annotations

__version__ = "0.1.0"

class ContextPacket(BaseModel):
    task_description: str
    recon_verdict: str
    source_urls: list[str] = Field(default_factory=list)
    files: list[ContextFile] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
