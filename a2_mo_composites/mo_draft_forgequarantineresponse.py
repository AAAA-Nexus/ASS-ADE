# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgequarantineresponse.py:7
# Component id: mo.source.a2_mo_composites.forgequarantineresponse
from __future__ import annotations

__version__ = "0.1.0"

class ForgeQuarantineResponse(NexusModel):
    """POST /v1/forge/quarantine"""
    quarantined: Any = None
    model_id: str | None = None
    reason: str | None = None
    count: int | None = None
