# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:686
# Component id: mo.source.a2_mo_composites.certify_output
from __future__ import annotations

__version__ = "0.1.0"

def certify_output(self, output: str, rubric: list[str], **kwargs: Any) -> CertifiedOutput:
    """/v1/certify/output — 30-day output certificate (OCN-100). $0.060/call"""
    return self._post_model("/v1/certify/output", CertifiedOutput, {"output": output, "rubric": rubric, **kwargs})
