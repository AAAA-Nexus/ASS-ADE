# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_federation_mint.py:7
# Component id: at.source.a1_at_functions.federation_mint
from __future__ import annotations

__version__ = "0.1.0"

def federation_mint(
    self,
    identity: dict | None = None,
    platforms: list[str] | None = None,
    *,
    agent_id: str | None = None,
    scope: str | None = None,
    **kwargs: Any,
) -> FederationToken:
    """/v1/federation/mint — cross-platform nxf_ identity token (AIF-100). $0.040/call"""
    resolved_identity = identity or ({"agent_id": agent_id} if agent_id else {})
    resolved_platforms = platforms or ([scope] if scope else [])
    return self._post_model("/v1/federation/mint", FederationToken, {"identity": resolved_identity, "platforms": resolved_platforms, **kwargs})
