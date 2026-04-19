# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1767
# Component id: at.source.ass_ade.escrow_status
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
