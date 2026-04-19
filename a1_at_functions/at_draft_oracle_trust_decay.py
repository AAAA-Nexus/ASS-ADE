# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1405
# Component id: at.source.ass_ade.oracle_trust_decay
from __future__ import annotations

__version__ = "0.1.0"

def oracle_trust_decay(
    agent_id: str = typer.Argument(..., help="Agent ID to score."),
    epochs: int = typer.Option(1, help="Epochs elapsed since last score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """P2P trust decay oracle. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_decay(agent_id=agent_id, epochs=epochs)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
