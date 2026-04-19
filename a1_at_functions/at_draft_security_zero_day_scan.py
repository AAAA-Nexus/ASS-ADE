# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3542
# Component id: at.source.ass_ade.security_zero_day_scan
__version__ = "0.1.0"

def security_zero_day_scan(
    payload_path: Annotated[Path, typer.Argument(help="Path to JSON payload to scan.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Zero-day pattern detector for agent payloads. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.security_zero_day(payload=payload)
    except (httpx.HTTPError, json.JSONDecodeError, OSError) as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc
    _print_json(result)
