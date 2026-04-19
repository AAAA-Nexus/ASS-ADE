# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:478
# Component id: mo.source.ass_ade.rng_verify
from __future__ import annotations

__version__ = "0.1.0"

def rng_verify(self, seed_ts: str, numbers: str, proof: str) -> dict:
    """/v1/rng/verify — verify HMAC proof offline. Free"""
    return self._get_model(  # type: ignore[return-value]
        "/v1/rng/verify", RngResult, seed_ts=seed_ts, numbers=numbers, proof=proof
    ).model_dump()
