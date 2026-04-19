# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2305
# Component id: at.source.ass_ade.defi_risk_score
from __future__ import annotations

__version__ = "0.1.0"

def defi_risk_score(
    protocol: str = typer.Argument(..., help="Protocol name or address."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """DeFi protocol risk score. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_risk_score(protocol=protocol)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
