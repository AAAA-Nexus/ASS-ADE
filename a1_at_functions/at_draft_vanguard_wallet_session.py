# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3652
# Component id: at.source.ass_ade.vanguard_wallet_session
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_wallet_session(
    agent_id: Annotated[str, typer.Argument(help="Agent ID.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Start a VANGUARD wallet session. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.vanguard_start_session(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
