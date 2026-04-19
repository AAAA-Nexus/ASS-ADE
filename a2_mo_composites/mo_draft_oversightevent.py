# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:791
# Component id: mo.source.ass_ade.oversightevent
from __future__ import annotations

__version__ = "0.1.0"

class OversightEvent(NexusModel):
    """/v1/compliance/oversight — OVS-100"""
    event_id: str | None = None
    attestation: str | None = None
    reviewer: str | None = None
    timestamp: str | None = None
