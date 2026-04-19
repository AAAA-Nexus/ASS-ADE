# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:504
# Component id: mo.source.ass_ade.quarantineresult
from __future__ import annotations

__version__ = "0.1.0"

class QuarantineResult(NexusModel):
    """/v1/agent/quarantine"""
    quarantined: bool | None = None
    agent_id: str | None = None
    reason: str | None = None
