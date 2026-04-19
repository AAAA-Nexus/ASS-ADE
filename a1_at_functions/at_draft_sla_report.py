# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1917
# Component id: at.source.ass_ade.sla_report
__version__ = "0.1.0"

def sla_report(
    sla_id: str = typer.Argument(..., help="SLA ID."),
    metric: str = typer.Argument(..., help="Metric name to report (e.g. 'uptime', 'latency_ms')."),
    value: float = typer.Argument(..., help="Observed metric value."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Report SLA compliance metrics. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_report(sla_id=sla_id, metric=metric, value=value)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
