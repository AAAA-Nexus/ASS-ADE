# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ethics_check.py:7
# Component id: at.source.a1_at_functions.ethics_check
from __future__ import annotations

__version__ = "0.1.0"

def ethics_check(self, text: str, **kwargs: Any) -> EthicsCheckResult:
    """/v1/ethics/check — Prime Axiom ethical oracle (DCM-1017). $0.040/request"""
    return self._post_model("/v1/ethics/check", EthicsCheckResult, {"text": text, **kwargs})
