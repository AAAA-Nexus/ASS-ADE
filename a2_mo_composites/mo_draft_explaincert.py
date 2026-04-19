# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_explaincert.py:7
# Component id: mo.source.a2_mo_composites.explaincert
from __future__ import annotations

__version__ = "0.1.0"

class ExplainCert(NexusModel):
    """/v1/compliance/explain — XPL-100"""
    certificate_id: str | None = None
    feature_attribution: dict | None = None
    gdpr_art22_ready: bool | None = None
