# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2606
# Component id: at.source.ass_ade.identity_sybil_check
from __future__ import annotations

__version__ = "0.1.0"

def identity_sybil_check(
    agent_id: str = typer.Argument(..., help="Agent ID to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Sybil resistance check (free trial). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sybil_check(actor=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Risk: {result.sybil_risk}  score={result.score}")
