# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_control_authorize.py:7
# Component id: at.source.a1_at_functions.control_authorize
from __future__ import annotations

__version__ = "0.1.0"

def control_authorize(
    agent_id: str = typer.Argument(..., help="Agent ID requesting action."),
    action: str = typer.Argument(..., help="Action to authorize."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Authorize an agent action. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.authorize_action(agent_id=agent_id, action=action)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
