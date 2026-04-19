# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:777
# Component id: mo.source.ass_ade.explaincert
from __future__ import annotations

__version__ = "0.1.0"

class ExplainCert(NexusModel):
    """/v1/compliance/explain — XPL-100"""
    certificate_id: str | None = None
    feature_attribution: dict | None = None
    gdpr_art22_ready: bool | None = None
