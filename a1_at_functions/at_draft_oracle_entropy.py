# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1275
# Component id: at.source.ass_ade.oracle_entropy
from __future__ import annotations

__version__ = "0.1.0"

def oracle_entropy(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Session entropy oracle. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.entropy_oracle()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
