# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_escrow_status.py:7
# Component id: at.source.a1_at_functions.escrow_status
from __future__ import annotations

__version__ = "0.1.0"

def escrow_status(
    escrow_id: str = typer.Argument(..., help="Escrow ID to inspect."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Check escrow status (funded/released/disputed/resolved). $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_status(escrow_id=escrow_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Escrow {escrow_id}")
    table.add_row("Status", str(result.status))
    table.add_row("Amount USDC", str(result.amount_usdc))
    console.print(table)
