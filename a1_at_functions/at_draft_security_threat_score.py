# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1592
# Component id: at.source.ass_ade.security_threat_score
__version__ = "0.1.0"

def security_threat_score(
    payload_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="JSON file containing the payload to score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Multi-vector threat scoring (SEC-303). $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload file: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.threat_score(payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="Threat Score")
    table.add_row("Level", str(result.threat_level))
    table.add_row("Score", str(result.score))
    console.print(table)
