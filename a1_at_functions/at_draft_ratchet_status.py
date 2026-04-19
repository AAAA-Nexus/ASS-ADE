# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1468
# Component id: at.source.ass_ade.ratchet_status
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_status(
    session_id: str = typer.Argument(..., help="Session ID to inspect."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Read RatchetGate session status + epoch. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            status = client.ratchet_status(session_id=session_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(status.model_dump())
