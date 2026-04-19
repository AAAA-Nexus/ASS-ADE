# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2206
# Component id: at.source.ass_ade.compliance_fairness
from __future__ import annotations

__version__ = "0.1.0"

def compliance_fairness(
    model_id: str = typer.Argument(..., help="Model ID to assess."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Fairness proof (disparate impact analysis). $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_fairness(model_id=model_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
