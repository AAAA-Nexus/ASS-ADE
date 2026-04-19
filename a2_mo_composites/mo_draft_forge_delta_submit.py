# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1359
# Component id: mo.source.ass_ade.forge_delta_submit
__version__ = "0.1.0"

    def forge_delta_submit(self, agent_id: str, delta: dict, **kwargs: Any) -> ForgeDeltaSubmitResult:
        """POST /v1/forge/delta/submit — submit improvement delta. Free."""
        return self._post_model("/v1/forge/delta/submit", ForgeDeltaSubmitResult, {"agent_id": agent_id, "delta": delta, **kwargs})
