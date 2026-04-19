# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:688
# Component id: mo.source.ass_ade.ethics_check
from __future__ import annotations

__version__ = "0.1.0"

def ethics_check(self, text: str, **kwargs: Any) -> EthicsCheckResult:
    """/v1/ethics/check — Prime Axiom ethical oracle (DCM-1017). $0.040/request"""
    return self._post_model("/v1/ethics/check", EthicsCheckResult, {"text": text, **kwargs})
