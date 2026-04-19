# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_ratchet_register.py:7
# Component id: at.source.a1_at_functions.ratchet_register
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_register(
    agent_id: str = typer.Argument(..., help="Agent ID to create a session for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write session JSON to this path."),
) -> None:
    """Register a new RatchetGate session. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    numeric_id = int(agent_id) if agent_id.isdigit() else (
        int.from_bytes(hashlib.sha256(agent_id.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF
    )
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            session = client.ratchet_register(agent_id=numeric_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(session.model_dump())
    if json_out:
        data = session.model_dump()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(data, indent=2), encoding="utf-8")
