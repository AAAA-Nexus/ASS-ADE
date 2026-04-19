# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3599
# Component id: at.source.ass_ade.data_convert
from __future__ import annotations

__version__ = "0.1.0"

def data_convert(
    input_path: Annotated[Path, typer.Argument(help="Input file.")],
    target_format: Annotated[str, typer.Argument(help="Target format (yaml, toml, etc).")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Convert structured data formats. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        content = input_path.read_text(encoding="utf-8")
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.data_convert(content=content, target_format=target_format)
    except (httpx.HTTPError, OSError) as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc
    _print_json(result)
