# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2587
# Component id: at.source.ass_ade.identity_verify
__version__ = "0.1.0"

def identity_verify(
    agent_id: str = typer.Argument(..., help="Agent ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify agent identity (allow/deny/flag). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.identity_verify(actor=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Decision: {result.decision}  uniqueness={result.uniqueness_coefficient}")
