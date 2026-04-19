# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1156
# Component id: mo.source.a2_mo_composites.forge_verify
from __future__ import annotations

__version__ = "0.1.0"

def forge_verify(self, agent_id: str, **kwargs: Any) -> ForgeVerifyResult:
    """POST /v1/forge/verify — verify an agent for Forge badge. Free."""
    return self._post_model("/v1/forge/verify", ForgeVerifyResult, {"agent_id": agent_id, **kwargs})
