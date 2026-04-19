# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:482
# Component id: mo.source.ass_ade.aibomdriftresult
from __future__ import annotations

__version__ = "0.1.0"

class AibomDriftResult(NexusModel):
    """/v1/aibom/drift"""
    drift_detected: bool | None = None
    lineage_hash: str | None = None
    verification_status: str | None = None
