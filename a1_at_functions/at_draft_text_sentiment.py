# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1570
# Component id: at.source.ass_ade.text_sentiment
__version__ = "0.1.0"

def text_sentiment(
    text: str = typer.Argument(..., help="Text to classify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Sentiment analysis — positive / negative / neutral. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_sentiment(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"{result.sentiment}  (confidence: {result.confidence})")
