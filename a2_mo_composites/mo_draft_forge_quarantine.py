# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1160
# Component id: mo.source.a2_mo_composites.forge_quarantine
from __future__ import annotations

__version__ = "0.1.0"

def forge_quarantine(self, model_id: str = "", reason: str = "probe", **kwargs: Any) -> ForgeQuarantineResponse:
    """POST /v1/forge/quarantine — quarantine a model. Free."""
    return self._post_model("/v1/forge/quarantine", ForgeQuarantineResponse, {"model_id": model_id, "reason": reason, **kwargs})
