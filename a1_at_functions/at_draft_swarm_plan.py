# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2041
# Component id: at.source.ass_ade.swarm_plan
__version__ = "0.1.0"

def swarm_plan(
    goal: str = typer.Argument(..., help="Goal to plan for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Generate a multi-step agent plan. $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_plan(goal=goal)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    for i, step in enumerate(result.steps, 1):
        console.print(f"{i}. {step}")
