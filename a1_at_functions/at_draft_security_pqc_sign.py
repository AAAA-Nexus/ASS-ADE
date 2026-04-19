# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_security_pqc_sign.py:7
# Component id: at.source.a1_at_functions.security_pqc_sign
from __future__ import annotations

__version__ = "0.1.0"

def security_pqc_sign(
    data: str = typer.Argument(..., help="Data string to sign with ML-DSA (Dilithium)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write signature JSON to this path."),
) -> None:
    """Post-quantum ML-DSA (Dilithium) signature. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.security_pqc_sign(data=data)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    d = result.model_dump()
    _print_json(d)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(d, indent=2), encoding="utf-8")
