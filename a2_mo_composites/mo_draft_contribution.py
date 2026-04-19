# Extracted from C:/!ass-ade/src/ass_ade/agent/lora_flywheel.py:35
# Component id: mo.source.ass_ade.contribution
from __future__ import annotations

__version__ = "0.1.0"

class Contribution:
    kind: str          # "fix", "principle", "rejection"
    content: dict[str, Any]
    ts: float = field(default_factory=time.time)
    session_id: str = ""
    confidence: float = 1.0
