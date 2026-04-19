# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:807
# Component id: mo.source.a2_mo_composites.defi_oracle_verify
from __future__ import annotations

__version__ = "0.1.0"

def defi_oracle_verify(
    self,
    pool: str | None = None,
    tvl_usdc: float = 0.0,
    *,
    oracle_id: str | None = None,
    **kwargs: Any,
) -> DefiOracleVerify:
    """/v1/defi/oracle-verify — flash loan + TWAP attack scoring (OGD-100). $0.04 + 0.1% TVL"""
    return self._post_model("/v1/defi/oracle-verify", DefiOracleVerify, {"pool": pool or oracle_id or "", "tvl_usdc": tvl_usdc, **kwargs})
