# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1290
# Component id: mo.source.ass_ade.bitnet_status
__version__ = "0.1.0"

    def bitnet_status(self, **kwargs: Any) -> BitNetStatus:
        """GET /v1/bitnet/status — BitNet engine health and metrics (BIT-105). Free."""
        return self._get_model("/v1/bitnet/status", BitNetStatus, **kwargs)
