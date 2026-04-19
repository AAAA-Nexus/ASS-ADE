# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2667
# Component id: at.source.ass_ade.vrf_verify
from __future__ import annotations

__version__ = "0.1.0"

def vrf_verify(
    draw_id: str = typer.Argument(..., help="Draw ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a VRF draw proof. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vrf_verify_draw(draw_id=draw_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Valid: {result.valid}")
