# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_verify.py:7
# Component id: at.source.a1_at_functions.verify
from __future__ import annotations

__version__ = "0.1.0"

def verify(self, code: str, spec: str) -> bool:
    if self._nexus is not None and hasattr(self._nexus, "certify_output_verify"):
        try:
            result = self._nexus.certify_output_verify(code)
            verdict = getattr(result, "rubric_passed", None)
            if verdict is not None:
                return bool(verdict)
        except Exception:
            pass
    metrics = _score(code, spec)
    return _passes(metrics)
