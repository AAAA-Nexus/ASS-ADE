# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1239
# Component id: mo.source.ass_ade.certify_codebase
__version__ = "0.1.0"

    def certify_codebase(
        self,
        local_certificate: dict[str, Any],
        agent_id: str | None = None,
    ) -> CertifyResult:
        """Sign and certify a codebase via AAAA-Nexus PQC signing."""
        payload: dict[str, Any] = {"certificate": local_certificate}
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/certify/codebase", CertifyResult, payload)
