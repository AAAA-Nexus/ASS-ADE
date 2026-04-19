# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3078
# Component id: at.source.ass_ade.dev_routing_think
__version__ = "0.1.0"

def dev_routing_think(
    query: str = typer.Argument(..., help="Query to route."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Model routing think-through. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.routing_think(query=query)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
