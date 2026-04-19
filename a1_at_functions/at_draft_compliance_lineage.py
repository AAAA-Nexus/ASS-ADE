# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compliance_lineage.py:7
# Component id: at.source.a1_at_functions.compliance_lineage
from __future__ import annotations

__version__ = "0.1.0"

def compliance_lineage(self, dataset_stages: list[dict], **kwargs: Any) -> LineageProof:
    """/v1/compliance/lineage — SHA-256 hash chain across dataset (LIN-100). $0.040/call"""
    return self._post_model("/v1/compliance/lineage", LineageProof, {"dataset_stages": dataset_stages, **kwargs})
