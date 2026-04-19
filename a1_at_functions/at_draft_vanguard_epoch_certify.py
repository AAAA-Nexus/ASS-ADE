# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3629
# Component id: at.source.ass_ade.vanguard_epoch_certify
__version__ = "0.1.0"

def vanguard_epoch_certify(
    system_id: Annotated[str, typer.Argument(help="System ID to certify.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Certify epoch drift + compliance. $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.aegis_certify_epoch(system_id=system_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
