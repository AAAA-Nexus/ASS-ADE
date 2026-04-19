# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1071
# Component id: mo.source.a2_mo_composites.bitnet_models
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_models(self, **kwargs: Any) -> BitNetModelsResponse:
    """GET /v1/bitnet/models — list available 1.58-bit models (BIT-102). Free."""
    return self._get_model("/v1/bitnet/models", BitNetModelsResponse, **kwargs)
