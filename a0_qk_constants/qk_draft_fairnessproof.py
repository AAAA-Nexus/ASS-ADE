# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:770
# Component id: qk.source.ass_ade.fairnessproof
from __future__ import annotations

__version__ = "0.1.0"

class FairnessProof(NexusModel):
    """/v1/compliance/fairness — FNS-100"""
    disparate_impact_ratio: float | None = None
    within_bound: bool | None = None
    theorem: str | None = None   # "FNS-100-FairnessBound"
