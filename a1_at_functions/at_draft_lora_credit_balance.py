# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_credit_balance.py:7
# Component id: at.source.a1_at_functions.lora_credit_balance
from __future__ import annotations

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
