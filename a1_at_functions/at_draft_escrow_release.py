# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1748
# Component id: at.source.ass_ade.escrow_release
__version__ = "0.1.0"

def escrow_release(
    escrow_id: str = typer.Argument(..., help="Escrow ID to release."),
    proof: str = typer.Option("", help="Release proof or authorization token."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Release funds from escrow to payee. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_release(escrow_id=escrow_id, proof=proof)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
