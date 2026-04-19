# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_contribute.py:7
# Component id: at.source.a1_at_functions.lora_contribute
from __future__ import annotations

__version__ = "0.1.0"

def lora_contribute(
    self,
    samples: list[dict[str, Any]],
    *,
    agent_id: str | None = None,
    trust_floor_threshold: float | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """POST /v1/lora/contribute — submit batch of privacy-scrubbed code fixes.

    Each sample: {digest, bad, good, lint_delta, language, size, ts}.
    Returns: {accepted, rejected, batch_size, agent_id, tau_threshold_used, reject_summary}.
    """
    payload: dict[str, Any] = {"samples": samples}
    if agent_id is not None:
        payload["agent_id"] = agent_id
    if trust_floor_threshold is not None:
        payload["trust_floor_threshold"] = trust_floor_threshold
    payload.update(kwargs)
    return self._post_raw("/v1/lora/contribute", payload)
