# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1789
# Component id: at.source.ass_ade.escrow_dispute
from __future__ import annotations

__version__ = "0.1.0"

def escrow_dispute(
    escrow_id: str = typer.Argument(..., help="Escrow ID to dispute."),
    reason: str = typer.Argument(..., help="Reason for dispute."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Open an escrow dispute. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_dispute(escrow_id=escrow_id, reason=reason)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
