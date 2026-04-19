# Extracted from C:/!ass-ade/src/ass_ade/agent/dgm_h.py:31
# Component id: mo.source.ass_ade.patch
from __future__ import annotations

__version__ = "0.1.0"

class Patch:
    id: str
    target: str
    diff: str
    kind: str = "code"
