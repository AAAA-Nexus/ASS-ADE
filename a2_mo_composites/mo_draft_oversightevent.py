# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_oversightevent.py:7
# Component id: mo.source.a2_mo_composites.oversightevent
from __future__ import annotations

__version__ = "0.1.0"

class OversightEvent(NexusModel):
    """/v1/compliance/oversight — OVS-100"""
    event_id: str | None = None
    attestation: str | None = None
    reviewer: str | None = None
    timestamp: str | None = None
