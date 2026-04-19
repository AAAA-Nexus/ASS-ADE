# Extracted from C:/!ass-ade/src/ass_ade/recon.py:91
# Component id: mo.source.ass_ade.researchtarget
from __future__ import annotations

__version__ = "0.1.0"

class ResearchTarget(BaseModel):
    topic: str
    query: str
    suggested_url: str | None = None
    status: str = "required"
