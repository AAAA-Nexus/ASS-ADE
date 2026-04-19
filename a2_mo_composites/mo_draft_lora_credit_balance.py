# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1441
# Component id: mo.source.ass_ade.lora_credit_balance
__version__ = "0.1.0"

    def lora_credit_balance(self, agent_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/credit/balance — current Nexus credit balance for an agent.

        Returns: {agent_id, balance_micro_usdc, balance_usdc, reward_model}.
        """
        headers = {"X-Agent-Id": agent_id} if agent_id else {}
        if headers:
            # One-off header override; use the underlying client directly
            response = self._client.get("/v1/lora/credit/balance", headers=headers, params=kwargs)
        else:
            response = self._client.get("/v1/lora/credit/balance", params=kwargs)
        response.raise_for_status()
        return response.json()
