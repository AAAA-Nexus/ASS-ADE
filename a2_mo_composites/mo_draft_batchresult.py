# Extracted from C:/!ass-ade/src/ass_ade/agent/lora_flywheel.py:44
# Component id: mo.source.ass_ade.batchresult
from __future__ import annotations

__version__ = "0.1.0"

class BatchResult:
    submitted: int
    contribution_id: str | None
    error: str | None = None
    reward_claimed: bool = False
