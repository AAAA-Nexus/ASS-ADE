# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2751
# Component id: at.source.ass_ade.bitnet_benchmark
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_benchmark(
    model: str = typer.Argument(..., help="BitNet model ID to benchmark."),
    n_tokens: int = typer.Option(100, help="Tokens to generate for benchmark."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Run inference benchmark for a 1.58-bit model (BIT-103). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_benchmark(model=model, n_tokens=n_tokens)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"BitNet Benchmark — {model}")
    table.add_row("Tokens/sec", str(result.tokens_per_second))
    table.add_row("Memory MB", str(result.memory_mb))
    table.add_row("Latency ms", str(result.latency_ms))
    console.print(table)
