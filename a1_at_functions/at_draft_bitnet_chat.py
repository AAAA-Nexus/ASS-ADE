# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:2713
# Component id: at.source.ass_ade.bitnet_chat
__version__ = "0.1.0"

def bitnet_chat(
    prompt: str = typer.Argument(..., help="Prompt for 1.58-bit inference."),
    model: str = typer.Option("bitnet-b1.58-2B-4T", help="BitNet model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """1.58-bit BitNet chat completion (BIT-100). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_inference(prompt=prompt, model=model)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(result.result or "(no response)")
