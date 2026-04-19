# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1398
# Component id: mo.source.ass_ade.lora_reward_claim
__version__ = "0.1.0"

    def lora_reward_claim(
        self,
        agent_id: str | None = None,
        *,
        contribution_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/lora/reward/claim — claim USDC payout for accepted samples."""
        payload: dict[str, Any] = {}
        if agent_id is not None:
            payload["agent_id"] = agent_id
        if contribution_id is not None:
            payload["contribution_id"] = contribution_id
        payload.update(kwargs)
        return self._post_raw("/v1/lora/reward/claim", payload)
