# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1390
# Component id: mo.source.ass_ade.lora_status
__version__ = "0.1.0"

    def lora_status(self, **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/status — current training-run info."""
        return self._get_raw("/v1/lora/status", **kwargs)
