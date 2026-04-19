# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_forge_quarantine.py:7
# Component id: at.source.a1_at_functions.forge_quarantine
from __future__ import annotations

__version__ = "0.1.0"

def forge_quarantine(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List quarantined agents. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_quarantine()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Quarantined agents: {result.count}")
    _print_json(result.quarantined)
