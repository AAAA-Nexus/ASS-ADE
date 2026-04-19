# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1437
# Component id: mo.source.ass_ade.lora_buffer_inspect
from __future__ import annotations

__version__ = "0.1.0"

def lora_buffer_inspect(self, **kwargs: Any) -> dict[str, Any]:
    """GET /v1/lora/buffer/inspect — show pending samples in the training buffer."""
    return self._get_raw("/v1/lora/buffer/inspect", **kwargs)
