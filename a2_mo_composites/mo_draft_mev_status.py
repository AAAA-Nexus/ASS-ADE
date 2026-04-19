# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1341
# Component id: mo.source.ass_ade.mev_status
__version__ = "0.1.0"

    def mev_status(self, bundle_id: str, **kwargs: Any) -> MevStatusResult:
        """GET /v1/mev/status — check MEV protection status for a bundle (MEV-101). Free."""
        return self._get_model("/v1/mev/status", MevStatusResult, bundle_id=bundle_id, **kwargs)
