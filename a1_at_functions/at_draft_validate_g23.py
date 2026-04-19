# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_g23.py:7
# Component id: at.source.a1_at_functions.validate_g23
from __future__ import annotations

__version__ = "0.1.0"

def validate_g23(self, intent: str, impl: str) -> bool:
    vi = vector_embed(intent)
    vc = vector_embed(impl)
    sim = _cosine(vi, vc)
    distance = max(0.0, 1.0 - sim) * 10.0
    return distance <= self._g23_threshold
