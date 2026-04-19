# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1711
# Component id: at.source.ass_ade.llm_stream
__version__ = "0.1.0"

def llm_stream(
    prompt: str = typer.Argument(..., help="Prompt to stream from Llama 3.1 8B."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Streaming chain-of-thought inference. $0.100/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            for chunk in client.inference_stream(prompt=prompt):
                console.print(chunk, end="")
    except httpx.HTTPError as exc:
        _nexus_err(exc)
