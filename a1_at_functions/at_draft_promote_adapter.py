# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_promote_adapter.py:7
# Component id: at.source.a1_at_functions.promote_adapter
from __future__ import annotations

__version__ = "0.1.0"

def promote_adapter(
    cfg: TrainConfig,
    adapter_url: str,
    weights_sha256: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    version = f"v{int(time.time())}"
    body = {
        "language": cfg.language,
        "base_model": cfg.base_model,
        "adapter_url": adapter_url,
        "weights_sha256": weights_sha256,
        "version": version,
        "metrics": metrics,
    }
    headers = {"X-Atomadic-Auth": cfg.owner_token or ""}
    url = f"{cfg.storefront_url.rstrip('/')}/v1/lora/adapter/promote"
    resp = httpx.post(url, headers=headers, json=body, timeout=30.0)
    resp.raise_for_status()
    return resp.json()
