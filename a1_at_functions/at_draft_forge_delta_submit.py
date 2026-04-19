# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2993
# Component id: at.source.ass_ade.forge_delta_submit
__version__ = "0.1.0"

def forge_delta_submit(
    agent_id: str = typer.Argument(..., help="Agent ID submitting the delta."),
    delta_file: Path = typer.Argument(..., exists=True, help="JSON file with improvement delta."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Submit an improvement delta for reward. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        delta = json.loads(delta_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read delta file: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_delta_submit(agent_id=agent_id, delta=delta)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
