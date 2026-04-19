# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2242
# Component id: at.source.ass_ade.compliance_drift_cert
from __future__ import annotations

__version__ = "0.1.0"

def compliance_drift_cert(
    model_id: str = typer.Argument(..., help="Model ID to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Issue drift-free certificate. $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.drift_certificate(model_id=model_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
