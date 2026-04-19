# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1449
# Component id: at.source.ass_ade.ratchet_advance
__version__ = "0.1.0"

def ratchet_advance(
    session_id: str = typer.Argument(..., help="Session ID to advance."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Advance epoch + re-key a RatchetGate session. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.ratchet_advance(session_id=session_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
