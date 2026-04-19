# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:283
# Component id: mo.source.a2_mo_composites.rng_verify
from __future__ import annotations

__version__ = "0.1.0"

def rng_verify(self, seed_ts: str, numbers: str, proof: str) -> dict:
    """/v1/rng/verify — verify HMAC proof offline. Free"""
    return self._get_model(  # type: ignore[return-value]
        "/v1/rng/verify", RngResult, seed_ts=seed_ts, numbers=numbers, proof=proof
    ).model_dump()
