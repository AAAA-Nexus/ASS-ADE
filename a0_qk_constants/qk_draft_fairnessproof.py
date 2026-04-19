# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_fairnessproof.py:7
# Component id: qk.source.a0_qk_constants.fairnessproof
from __future__ import annotations

__version__ = "0.1.0"

class FairnessProof(NexusModel):
    """/v1/compliance/fairness — FNS-100"""
    disparate_impact_ratio: float | None = None
    within_bound: bool | None = None
    theorem: str | None = None   # "FNS-100-FairnessBound"
