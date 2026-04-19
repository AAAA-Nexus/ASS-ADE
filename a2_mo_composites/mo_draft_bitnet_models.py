# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1266
# Component id: mo.source.ass_ade.bitnet_models
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_models(self, **kwargs: Any) -> BitNetModelsResponse:
    """GET /v1/bitnet/models — list available 1.58-bit models (BIT-102). Free."""
    return self._get_model("/v1/bitnet/models", BitNetModelsResponse, **kwargs)
