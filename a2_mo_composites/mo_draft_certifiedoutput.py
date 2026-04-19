# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_certifiedoutput.py:7
# Component id: mo.source.a2_mo_composites.certifiedoutput
from __future__ import annotations

__version__ = "0.1.0"

class CertifiedOutput(NexusModel):
    """/v1/certify/output — OCN-100"""
    certificate_id: str | None = None
    score: float | None = None
    rubric_passed: bool | None = None
    valid_until: str | None = None
