# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2565
# Component id: at.source.ass_ade.control_federation_mint
from __future__ import annotations

__version__ = "0.1.0"

def control_federation_mint(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    scope: str = typer.Option("read", help="Token scope."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Mint a federated trust token. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.federation_mint(agent_id=agent_id, scope=scope)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
