# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_quarantineresult.py:7
# Component id: mo.source.a2_mo_composites.quarantineresult
from __future__ import annotations

__version__ = "0.1.0"

class QuarantineResult(NexusModel):
    """/v1/agent/quarantine"""
    quarantined: bool | None = None
    agent_id: str | None = None
    reason: str | None = None
