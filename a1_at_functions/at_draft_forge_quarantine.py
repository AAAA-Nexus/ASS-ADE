# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2975
# Component id: at.source.ass_ade.forge_quarantine
__version__ = "0.1.0"

def forge_quarantine(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List quarantined agents. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_quarantine()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Quarantined agents: {result.count}")
    _print_json(result.quarantined)
