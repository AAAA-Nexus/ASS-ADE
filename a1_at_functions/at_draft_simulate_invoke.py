# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_simulate_invoke.py:7
# Component id: at.source.a1_at_functions.simulate_invoke
from __future__ import annotations

__version__ = "0.1.0"

def simulate_invoke(base_url: str, tool: MCPTool, payload: Any | None = None) -> dict:
    """Return a simulation summary of invoking the given tool without network I/O.

    The result is a JSON-serializable dict suitable for printing to users or
    CI systems when doing a dry-run. Absolute endpoints are validated for SSRF safety.
    Raises ValueError if an absolute endpoint fails validation.
    """
    endpoint = tool.endpoint or ""
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        # Absolute endpoint: validate for SSRF safety
        url = _validate_absolute_endpoint(endpoint)
    else:
        url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")

    return {
        "simulated": True,
        "tool": tool.name,
        "method": (tool.method or "POST").upper(),
        "endpoint": url,
        "paid": bool(tool.paid),
        "payload_preview": payload,
        "note": "dry-run; no network request performed",
    }
