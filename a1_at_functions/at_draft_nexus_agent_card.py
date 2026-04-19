# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_nexus_agent_card.py:5
# Component id: at.source.ass_ade.nexus_agent_card
__version__ = "0.1.0"

def nexus_agent_card(
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
            _print_json(client.get_agent_card())
    except httpx.HTTPError as exc:
        _nexus_err(exc)
