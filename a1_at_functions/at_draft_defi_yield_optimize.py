# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2382
# Component id: at.source.ass_ade.defi_yield_optimize
__version__ = "0.1.0"

def defi_yield_optimize(
    amount_usdc: float = typer.Argument(..., help="Amount in USDC to optimize."),
    risk_tolerance: str = typer.Option("medium", help="low/medium/high"),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Yield optimization across DeFi protocols. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_yield_optimize(amount_usdc=amount_usdc, risk_tolerance=risk_tolerance)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
