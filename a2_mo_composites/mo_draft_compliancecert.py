# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:528
# Component id: mo.source.ass_ade.compliancecert
from __future__ import annotations

__version__ = "0.1.0"

class ComplianceCert(NexusModel):
    """/v1/aegis/certify-epoch (AEG-102 — 47-epoch drift + EU AI Act cert)"""
    certificate_id: str | None = None
    epoch: int | None = None
    eu_ai_act_compliant: bool | None = None
    drift_within_bound: bool | None = None
