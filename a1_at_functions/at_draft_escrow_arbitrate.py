# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1807
# Component id: at.source.ass_ade.escrow_arbitrate
__version__ = "0.1.0"

def escrow_arbitrate(
    escrow_id: str = typer.Argument(..., help="Escrow ID to arbitrate."),
    vote: str = typer.Option("release", help="Arbitration vote: 'release' or 'refund'."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Trigger automated arbitration. $0.100/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_arbitrate(escrow_id=escrow_id, vote=vote)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
