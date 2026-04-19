# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2449
# Component id: at.source.ass_ade.aegis_certify_epoch
__version__ = "0.1.0"

def aegis_certify_epoch(
    agent_id: str = typer.Argument(..., help="Agent ID to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Issue epoch compliance certificate (AEG-101). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.aegis_certify_epoch(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
