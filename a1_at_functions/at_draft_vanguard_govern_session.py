# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_vanguard_govern_session.py:7
# Component id: at.source.a1_at_functions.vanguard_govern_session
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_govern_session(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    wallet_address: str = typer.Argument(..., help="Wallet address."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """UCAN wallet session governance. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_govern_session(agent_id=agent_id, wallet=wallet_address)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
