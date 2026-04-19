# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:493
# Component id: mo.source.a2_mo_composites.ethics_check
from __future__ import annotations

__version__ = "0.1.0"

def ethics_check(self, text: str, **kwargs: Any) -> EthicsCheckResult:
    """/v1/ethics/check — Prime Axiom ethical oracle (DCM-1017). $0.040/request"""
    return self._post_model("/v1/ethics/check", EthicsCheckResult, {"text": text, **kwargs})
