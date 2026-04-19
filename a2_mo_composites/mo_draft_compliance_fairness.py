# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:865
# Component id: mo.source.a2_mo_composites.compliance_fairness
from __future__ import annotations

__version__ = "0.1.0"

def compliance_fairness(self, dataset_description: str | None = None, *, model_id: str | None = None, **kwargs: Any) -> FairnessProof:
    """/v1/compliance/fairness — disparate impact ratio (FNS-100). $0.040/check"""
    return self._post_model("/v1/compliance/fairness", FairnessProof, {"dataset_description": dataset_description or model_id or "", **kwargs})
