# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2907
# Component id: at.source.ass_ade.mev_status
__version__ = "0.1.0"

def mev_status(
    bundle_id: str = typer.Argument(..., help="Bundle ID to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Check MEV protection status for a bundle (MEV-101). Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.mev_status(bundle_id=bundle_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"MEV Bundle — {bundle_id}")
    table.add_row("Status", str(result.status))
    table.add_row("Block", str(result.included_in_block))
    table.add_row("MEV Saved USD", str(result.mev_saved_usd))
    console.print(table)
