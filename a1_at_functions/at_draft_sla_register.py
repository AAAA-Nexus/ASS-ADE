# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1895
# Component id: at.source.ass_ade.sla_register
__version__ = "0.1.0"

def sla_register(
    agent_id: str = typer.Argument(..., help="Agent ID to register SLA for."),
    uptime_pct: float = typer.Option(0.99, help="Uptime commitment (0.0–1.0)."),
    latency_ms: float = typer.Option(500.0, help="P99 latency commitment in ms."),
    error_rate: float = typer.Option(0.01, help="Acceptable error rate (0.0–1.0)."),
    bond_usdc: float = typer.Option(0.0, help="Bond amount in USDC staked against SLA."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Register a service-level agreement. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_register(agent_id=agent_id, latency_ms=latency_ms, uptime_pct=uptime_pct, error_rate=error_rate, bond_usdc=bond_usdc)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
