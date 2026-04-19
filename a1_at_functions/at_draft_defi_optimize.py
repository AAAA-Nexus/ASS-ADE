# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2282
# Component id: at.source.ass_ade.defi_optimize
from __future__ import annotations

__version__ = "0.1.0"

def defi_optimize(
    payload_file: Path = typer.Argument(..., exists=True, help="JSON DeFi portfolio payload."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """DeFi portfolio optimization (MVO). $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_optimize(payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
