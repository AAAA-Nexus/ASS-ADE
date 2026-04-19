# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2864
# Component id: at.source.ass_ade.vanguard_lock_and_verify
__version__ = "0.1.0"

def vanguard_lock_and_verify(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    amount: float = typer.Argument(..., help="Amount in USDC to lock."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Lock and verify an escrow (Vanguard). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_lock_and_verify(agent_id=agent_id, amount_usdc=amount)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
