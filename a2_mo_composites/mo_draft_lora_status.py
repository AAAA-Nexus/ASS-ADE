# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1390
# Component id: mo.source.ass_ade.lora_status
from __future__ import annotations

__version__ = "0.1.0"

def lora_status(self, **kwargs: Any) -> dict[str, Any]:
    """GET /v1/lora/status — current training-run info."""
    return self._get_raw("/v1/lora/status", **kwargs)
