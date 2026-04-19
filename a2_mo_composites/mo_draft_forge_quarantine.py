# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1355
# Component id: mo.source.ass_ade.forge_quarantine
from __future__ import annotations

__version__ = "0.1.0"

def forge_quarantine(self, model_id: str = "", reason: str = "probe", **kwargs: Any) -> ForgeQuarantineResponse:
    """POST /v1/forge/quarantine — quarantine a model. Free."""
    return self._post_model("/v1/forge/quarantine", ForgeQuarantineResponse, {"model_id": model_id, "reason": reason, **kwargs})
