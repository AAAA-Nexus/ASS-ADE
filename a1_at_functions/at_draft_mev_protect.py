# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2888
# Component id: at.source.ass_ade.mev_protect
from __future__ import annotations

__version__ = "0.1.0"

def mev_protect(
    tx_bundle_csv: str = typer.Argument(..., help="Comma-separated transaction hex strings."),
    strategy: str = typer.Option("flashbots", help="Protection strategy: flashbots/private-mempool/time-delay."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Wrap a transaction bundle with MEV protection (MEV-100). $0.020/tx."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    tx_bundle = [t.strip() for t in tx_bundle_csv.split(",") if t.strip()]
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.mev_protect(tx_bundle=tx_bundle, strategy=strategy)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
