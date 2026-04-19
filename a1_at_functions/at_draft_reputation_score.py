# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_reputation_score.py:7
# Component id: at.source.a1_at_functions.reputation_score
from __future__ import annotations

__version__ = "0.1.0"

def reputation_score(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Get reputation score + tier. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.reputation_score(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Reputation — {agent_id}")
    table.add_row("Score", str(result.score))
    table.add_row("Tier", str(result.tier))
    table.add_row("Fee Multiplier", str(result.fee_multiplier))
    console.print(table)
