# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ethics_compliance.py:7
# Component id: at.source.a1_at_functions.ethics_compliance
from __future__ import annotations

__version__ = "0.1.0"

def ethics_compliance(self, system_description: str, **kwargs: Any) -> EthicsCheckResult:
    """/v1/ethics/compliance — Prime Axiom audit with formal proof of safety. $0.040/call"""
    return self._post_model("/v1/ethics/compliance", EthicsCheckResult, {"system_description": system_description, **kwargs})
