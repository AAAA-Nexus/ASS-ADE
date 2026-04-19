# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_defi_liquidation_check.py:7
# Component id: at.source.a1_at_functions.defi_liquidation_check
from __future__ import annotations

__version__ = "0.1.0"

def defi_liquidation_check(
    position_id: str = typer.Argument(..., help="DeFi position ID."),
    collateral: float = typer.Argument(..., help="Collateral value USD."),
    debt: float = typer.Argument(..., help="Debt value USD."),
    cf: float = typer.Option(0.80, help="Collateral factor."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Health factor + liquidation distance (LQS-100). $0.040/check."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_liquidation_check(
                position_id=position_id, collateral_value=collateral,
                debt_value=debt, collateral_factor=cf,
            )
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
