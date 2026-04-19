# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2490
# Component id: at.source.ass_ade.control_spending_authorize
__version__ = "0.1.0"

def control_spending_authorize(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    amount_usdc: float = typer.Argument(..., help="Amount to authorize in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Authorize a spending request. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.spending_authorize(agent_id=agent_id, amount_usdc=amount_usdc)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
