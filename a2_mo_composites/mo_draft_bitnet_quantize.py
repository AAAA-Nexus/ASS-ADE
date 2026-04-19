# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1091
# Component id: mo.source.a2_mo_composites.bitnet_quantize
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_quantize(self, model_id: str, **kwargs: Any) -> BitNetQuantizeResponse:
    """POST /v1/bitnet/quantize — convert model to 1.58-bit ternary weights (BIT-104). $0.100/call"""
    return self._post_model("/v1/bitnet/quantize", BitNetQuantizeResponse, {"model_id": model_id, **kwargs})
