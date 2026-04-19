# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:831
# Component id: mo.source.ass_ade.federation_mint
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
