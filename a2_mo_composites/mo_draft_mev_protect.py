# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1337
# Component id: mo.source.ass_ade.mev_protect
__version__ = "0.1.0"

    def mev_protect(self, tx_bundle: list[str], **kwargs: Any) -> MevProtectResult:
        """POST /v1/mev/protect — MEV protection for a transaction bundle (MEV-100). $0.020/tx"""
        return self._post_model("/v1/mev/protect", MevProtectResult, {"tx_bundle": tx_bundle, **kwargs})
