# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1068
# Component id: mo.source.ass_ade.compliance_lineage
from __future__ import annotations

__version__ = "0.1.0"

def compliance_lineage(self, dataset_stages: list[dict], **kwargs: Any) -> LineageProof:
    """/v1/compliance/lineage — SHA-256 hash chain across dataset (LIN-100). $0.040/call"""
    return self._post_model("/v1/compliance/lineage", LineageProof, {"dataset_stages": dataset_stages, **kwargs})
