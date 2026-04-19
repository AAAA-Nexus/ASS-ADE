# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1660
# Component id: at.source.ass_ade.security_pqc_sign
__version__ = "0.1.0"

def security_pqc_sign(
    data: str = typer.Argument(..., help="Data string to sign with ML-DSA (Dilithium)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write signature JSON to this path."),
) -> None:
    """Post-quantum ML-DSA (Dilithium) signature. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.security_pqc_sign(data=data)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    d = result.model_dump()
    _print_json(d)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(d, indent=2), encoding="utf-8")
