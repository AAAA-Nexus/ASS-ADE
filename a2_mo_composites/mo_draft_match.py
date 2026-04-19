# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_match.py:7
# Component id: mo.source.a2_mo_composites.match
from __future__ import annotations

__version__ = "0.1.0"

class Match:
    id: str
    score: float
    spec: str
    code: str
    proof: str
    metadata: dict[str, Any]
