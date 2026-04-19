# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2365
# Component id: sy.source.ass_ade.defi_bridge_verify
from __future__ import annotations

__version__ = "0.1.0"

def defi_bridge_verify(
    bridge_id: str = typer.Argument(..., help="Bridge transaction ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a cross-chain bridge transaction. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_bridge_verify(bridge_id=bridge_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
