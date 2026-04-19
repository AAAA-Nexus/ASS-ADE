# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1142
# Component id: mo.source.a2_mo_composites.mev_protect
from __future__ import annotations

__version__ = "0.1.0"

def mev_protect(self, tx_bundle: list[str], **kwargs: Any) -> MevProtectResult:
    """POST /v1/mev/protect — MEV protection for a transaction bundle (MEV-100). $0.020/tx"""
    return self._post_model("/v1/mev/protect", MevProtectResult, {"tx_bundle": tx_bundle, **kwargs})
