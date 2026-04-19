# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2645
# Component id: at.source.ass_ade.vrf_draw
__version__ = "0.1.0"

def vrf_draw(
    game_id: str = typer.Argument(..., help="Game or draw ID."),
    n: int = typer.Option(1, help="Number of integers to draw."),
    min_val: int = typer.Option(1, help="Minimum value (inclusive)."),
    max_val: int = typer.Option(100, help="Maximum value (inclusive)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verifiable random draw — provably fair. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vrf_draw(game_id=game_id, n=n, range_min=min_val, range_max=max_val)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
