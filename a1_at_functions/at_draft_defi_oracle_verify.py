# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2323
# Component id: at.source.ass_ade.defi_oracle_verify
from __future__ import annotations

__version__ = "0.1.0"

def defi_oracle_verify(
    oracle_id: str = typer.Argument(..., help="Oracle ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a price oracle for manipulation. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_oracle_verify(oracle_id=oracle_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
