# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1242
# Component id: mo.source.a2_mo_composites.lora_buffer_inspect
from __future__ import annotations

__version__ = "0.1.0"

def lora_buffer_inspect(self, **kwargs: Any) -> dict[str, Any]:
    """GET /v1/lora/buffer/inspect — show pending samples in the training buffer."""
    return self._get_raw("/v1/lora/buffer/inspect", **kwargs)
