# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:36
# Component id: mo.source.ass_ade.gapentry
from __future__ import annotations

__version__ = "0.1.0"

class GAPEntry:
    description: str
    ts: float = field(default_factory=time.time)
    source: str = ""
