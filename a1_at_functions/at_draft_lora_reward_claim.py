# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_reward_claim.py:7
# Component id: at.source.a1_at_functions.lora_reward_claim
from __future__ import annotations

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
