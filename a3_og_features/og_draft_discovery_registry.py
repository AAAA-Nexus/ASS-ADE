# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2021
# Component id: og.source.ass_ade.discovery_registry
from __future__ import annotations

__version__ = "0.1.0"

def discovery_registry(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List all registered agents. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.discovery_registry()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
