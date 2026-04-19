# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1473
# Component id: mo.source.ass_ade.enhance_apply
__version__ = "0.1.0"

    def enhance_apply(
        self,
        improvement_ids: list[int],
        local_report: dict[str, Any],
        agent_id: str | None = None,
    ) -> EnhanceApplyResult:
        """Apply selected enhancements: generate blueprints and trigger rebuild."""
        payload: dict[str, Any] = {
            "improvement_ids": improvement_ids,
            "local_report": local_report,
        }
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/enhance/apply", EnhanceApplyResult, payload)
