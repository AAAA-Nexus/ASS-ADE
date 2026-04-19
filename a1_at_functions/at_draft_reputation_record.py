# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1831
# Component id: at.source.ass_ade.reputation_record
from __future__ import annotations

__version__ = "0.1.0"

def reputation_record(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    success: bool = typer.Option(True, help="Whether the task succeeded."),
    quality: float = typer.Option(1.0, help="Quality score (0.0–1.0)."),
    latency_ms: float = typer.Option(0.0, help="Observed latency in milliseconds."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Record a reputation event. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.reputation_record(agent_id=agent_id, success=success, quality=quality, latency_ms=latency_ms)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
