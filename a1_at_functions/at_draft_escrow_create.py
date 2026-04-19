# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_escrow_create.py:7
# Component id: at.source.a1_at_functions.escrow_create
from __future__ import annotations

__version__ = "0.1.0"

def escrow_create(
    payer: str = typer.Argument(..., help="Payer agent ID."),
    payee: str = typer.Argument(..., help="Payee agent ID."),
    amount: float = typer.Argument(..., help="Amount in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Create a new on-chain escrow contract. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_create(amount_usdc=amount, sender=payer, receiver=payee, conditions=[])
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
