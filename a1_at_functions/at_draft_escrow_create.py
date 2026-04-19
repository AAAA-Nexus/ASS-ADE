# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1728
# Component id: at.source.ass_ade.escrow_create
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
