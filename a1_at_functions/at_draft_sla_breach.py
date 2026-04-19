# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1956
# Component id: at.source.ass_ade.sla_breach
from __future__ import annotations

__version__ = "0.1.0"

def sla_breach(
    sla_id: str = typer.Argument(..., help="SLA ID."),
    severity: str = typer.Option("medium", help="Breach severity: minor/medium/critical."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Report an SLA breach and trigger penalty. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_breach(sla_id=sla_id, severity=severity)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
