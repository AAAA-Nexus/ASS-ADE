# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_swarm_relay.py:7
# Component id: at.source.a1_at_functions.swarm_relay
from __future__ import annotations

__version__ = "0.1.0"

def swarm_relay(
    sender: str = typer.Argument(..., help="Sender agent ID."),
    recipients_csv: str = typer.Argument(..., help="Comma-separated recipient agent IDs."),
    message: str = typer.Argument(..., help="Message to relay."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Relay a message through the agent swarm. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    recipients = [r.strip() for r in recipients_csv.split(",") if r.strip()]
    to = recipients[0] if recipients else ""
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.swarm_relay(from_id=sender, to=to, message={"text": message, "recipients": recipients})
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
