# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_nexus_mcp_manifest.py:5
# Component id: qk.source.ass_ade.nexus_mcp_manifest
__version__ = "0.1.0"

def nexus_mcp_manifest(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            _print_json(client.get_mcp_manifest())
    except httpx.HTTPError as exc:
        _nexus_err(exc)
