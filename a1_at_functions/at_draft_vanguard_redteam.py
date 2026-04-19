# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2795
# Component id: at.source.ass_ade.vanguard_redteam
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_redteam(
    agent_id: str = typer.Argument(..., help="Agent ID to red-team."),
    target: str = typer.Argument(..., help="Target system or endpoint."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Continuous red-team audit for an agent. $0.100/run."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_redteam(agent_id=agent_id, target=target)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Red-Team Audit — {agent_id}")
    table.add_row("Vulnerabilities", str(result.vulnerabilities_found))
    table.add_row("Severity", str(result.severity))
    table.add_row("Run ID", str(result.run_id))
    console.print(table)
    if result.findings:
        _print_json(result.findings)
