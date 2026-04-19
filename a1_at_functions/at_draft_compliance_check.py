# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2163
# Component id: at.source.ass_ade.compliance_check
__version__ = "0.1.0"

def compliance_check(
    payload_file: Path = typer.Argument(..., exists=True, help="JSON payload to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Multi-framework compliance check. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_check(system_description=json.dumps(payload))
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
