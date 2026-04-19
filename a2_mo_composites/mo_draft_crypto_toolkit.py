# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1014
# Component id: mo.source.a2_mo_composites.crypto_toolkit
from __future__ import annotations

__version__ = "0.1.0"

def crypto_toolkit(self, data: str, **kwargs: Any) -> CryptoToolkit:
    """/v1/dcm/crypto-toolkit — BLAKE3 + Merkle proof + nonce (DCM-1018). $0.020/call"""
    return self._post_model("/v1/dcm/crypto-toolkit", CryptoToolkit, {"data": data, **kwargs})
