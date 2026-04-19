# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:279
# Component id: mo.source.a2_mo_composites.rng_quantum
from __future__ import annotations

__version__ = "0.1.0"

def rng_quantum(self, count: int = 1, **kwargs: Any) -> RngResult:
    """/v1/rng/quantum — quantum-seeded RNG with proof. $0.020/request"""
    return self._get_model("/v1/rng/quantum", RngResult, count=count, **kwargs)
