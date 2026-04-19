# Extracted from C:/!ass-ade/src/ass_ade/cli.py:816
# Component id: at.source.ass_ade.nexus_health
from __future__ import annotations

__version__ = "0.1.0"

def nexus_health(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            _print_json(client.get_health())
    except httpx.HTTPError as exc:
        _nexus_err(exc)
