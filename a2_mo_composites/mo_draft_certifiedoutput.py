# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:653
# Component id: mo.source.ass_ade.certifiedoutput
from __future__ import annotations

__version__ = "0.1.0"

class CertifiedOutput(NexusModel):
    """/v1/certify/output — OCN-100"""
    certificate_id: str | None = None
    score: float | None = None
    rubric_passed: bool | None = None
    valid_until: str | None = None
