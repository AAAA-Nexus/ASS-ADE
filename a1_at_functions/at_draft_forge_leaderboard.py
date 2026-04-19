# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2934
# Component id: at.source.ass_ade.forge_leaderboard
from __future__ import annotations

__version__ = "0.1.0"

def forge_leaderboard(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Forge agent leaderboard. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_leaderboard()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="Forge Leaderboard")
    table.add_column("Rank", justify="right")
    table.add_column("Agent ID")
    table.add_column("Name")
    table.add_column("Score")
    for entry in result.entries:
        table.add_row(str(entry.rank or ""), entry.agent_id or "", entry.name or "", str(entry.score or ""))
    console.print(table)
