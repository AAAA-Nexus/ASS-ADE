# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1351
# Component id: mo.source.ass_ade.forge_verify
from __future__ import annotations

__version__ = "0.1.0"

def forge_verify(self, agent_id: str, **kwargs: Any) -> ForgeVerifyResult:
    """POST /v1/forge/verify — verify an agent for Forge badge. Free."""
    return self._post_model("/v1/forge/verify", ForgeVerifyResult, {"agent_id": agent_id, **kwargs})
