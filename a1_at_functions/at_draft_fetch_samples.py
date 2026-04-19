# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_fetch_samples.py:5
# Component id: at.source.ass_ade.fetch_samples
__version__ = "0.1.0"

def fetch_samples(cfg: TrainConfig) -> list[dict[str, Any]]:
    """Authenticated GET /v1/lora/samples/export — owner token required."""
    if not cfg.owner_token:
        raise RuntimeError(
            "AAAA_NEXUS_OWNER_TOKEN not set. Samples export is owner-only."
        )
    url = f"{cfg.storefront_url.rstrip('/')}/v1/lora/samples/export"
    headers = {"X-Atomadic-Auth": cfg.owner_token}
    params = {"lang": cfg.language, "limit": str(cfg.max_samples)}
    resp = httpx.get(url, headers=headers, params=params, timeout=60.0)
    resp.raise_for_status()
    data = resp.json()
    samples = data.get("samples") or []
    _log.info("fetched %d %s samples from storefront", len(samples), cfg.language)
    return samples
