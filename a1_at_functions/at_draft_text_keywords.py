# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1551
# Component id: at.source.ass_ade.text_keywords
__version__ = "0.1.0"

def text_keywords(
    text: str = typer.Argument(..., help="Text to extract keywords from."),
    top_k: int = typer.Option(10, help="Number of keywords to return."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """TF-IDF keyword extraction. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_keywords(text=text, top_k=top_k)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
