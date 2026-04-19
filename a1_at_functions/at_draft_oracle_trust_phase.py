# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1256
# Component id: at.source.ass_ade.oracle_trust_phase
__version__ = "0.1.0"

def oracle_trust_phase(
    agent_id: str = typer.Argument(..., help="Agent ID to score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """V_AI geometric trust phase oracle. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_phase_oracle(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
