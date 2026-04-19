# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2623
# Component id: at.source.ass_ade.identity_delegate_verify
__version__ = "0.1.0"

def identity_delegate_verify(
    token: str = typer.Argument(..., help="UCAN delegation token."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a UCAN delegation token. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.delegate_verify(token=token)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Valid: {result.valid}  depth={result.depth}/{result.depth_limit}")
