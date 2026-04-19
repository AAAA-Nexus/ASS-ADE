# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_contribution.py:7
# Component id: mo.source.a2_mo_composites.contribution
from __future__ import annotations

__version__ = "0.1.0"

class Contribution:
    kind: str          # "fix", "principle", "rejection"
    content: dict[str, Any]
    ts: float = field(default_factory=time.time)
    session_id: str = ""
    confidence: float = 1.0
