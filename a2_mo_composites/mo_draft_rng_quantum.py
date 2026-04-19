# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:474
# Component id: mo.source.ass_ade.rng_quantum
from __future__ import annotations

__version__ = "0.1.0"

def rng_quantum(self, count: int = 1, **kwargs: Any) -> RngResult:
    """/v1/rng/quantum — quantum-seeded RNG with proof. $0.020/request"""
    return self._get_model("/v1/rng/quantum", RngResult, count=count, **kwargs)
