# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2186
# Component id: at.source.ass_ade.compliance_eu_ai_act
__version__ = "0.1.0"

def compliance_eu_ai_act(
    system_name: str = typer.Argument(..., help="AI system name."),
    risk_level: str = typer.Option("limited", help="Risk level: minimal/limited/high/unacceptable."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """EU AI Act compliance assessment. $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_eu_ai_act(system_description=f"{system_name} (risk level: {risk_level})")
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
