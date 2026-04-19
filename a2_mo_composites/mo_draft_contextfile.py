# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_contextfile.py:7
# Component id: mo.source.a2_mo_composites.contextfile
from __future__ import annotations

__version__ = "0.1.0"

class ContextFile(BaseModel):
    path: str
    sha256: str
    size_bytes: int
    excerpt: str
    truncated: bool = False
