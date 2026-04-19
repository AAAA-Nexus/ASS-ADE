from __future__ import annotations

import time
from typing import Any

import httpx
import jsonschema
from jsonschema import ValidationError

from ass_ade.nexus.models import CostEstimate, MCPManifest, MCPTool
from ass_ade.nexus.validation import sanitize_header_value, validate_https_public_url


def _validate_absolute_endpoint(endpoint: str) -> str:
    """Validate absolute endpoint URLs against SSRF attack surface."""
    if not endpoint or endpoint.startswith("/"):
        return endpoint
    if not (endpoint.startswith("http://") or endpoint.startswith("https://")):
        return endpoint
    return validate_https_public_url(endpoint, field_name="Endpoint URL")


def resolve_tool(manifest: MCPManifest, identifier: str) -> MCPTool | None:
    """Resolve a tool by index (1-based) or name.

    identifier may be a numeric string referencing the manifest list index,
    or a tool name.
    """
    if identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(manifest.tools):
            return manifest.tools[idx]
        return None

    for tool in manifest.tools:
        if tool.name and tool.name.lower() == identifier.lower():
            return tool
    return None


def invoke_tool(
    base_url: str,
    tool: MCPTool,
    payload: Any | None = None,
    timeout: float = 20.0,
    retries: int = 3,
    backoff_base: float = 0.5,
    api_key: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> httpx.Response:
    """Invoke an MCP tool endpoint with exponential backoff retries.

    - If `tool.endpoint` is absolute, it is validated for SSRF safety before use.
    - Otherwise the endpoint is joined to `base_url`.
    - The method defaults to POST when unspecified.
    - Retries on 429 and 5xx responses using exponential backoff.
    - Raises ValueError if an absolute endpoint fails SSRF validation.
    """
    method = (tool.method or "POST").upper()
    endpoint = tool.endpoint or ""
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        # Absolute endpoint: validate for SSRF safety before use
        url = _validate_absolute_endpoint(endpoint)
    else:
        url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")

    headers: dict[str, str] = {"User-Agent": "ass-ade/1.0.0"}
    if api_key:
        safe_key = sanitize_header_value(api_key.strip(), "api_key")
        headers["Authorization"] = f"Bearer {safe_key}"
        headers["X-API-Key"] = safe_key

    last_exc: httpx.HTTPError | None = None
    with httpx.Client(timeout=timeout, headers=headers, transport=transport) as client:
        for attempt in range(max(1, retries)):
            try:
                if method == "GET":
                    response = client.get(url, params=payload)
                else:
                    response = client.request(method, url, json=payload)

                if response.status_code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                    time.sleep(backoff_base * (2 ** attempt))
                    continue

                return response
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt < retries - 1:
                    time.sleep(backoff_base * (2 ** attempt))

    if last_exc is not None:
        raise last_exc
    raise httpx.HTTPError("invoke_tool: all retries exhausted")


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


def estimate_cost(tool: MCPTool) -> CostEstimate | None:
    """Return the cost metadata for a tool, or None if the tool is free / metadata unavailable."""
    if tool.cost is not None:
        return tool.cost
    if bool(tool.paid):
        # Manifest declares paid but no cost detail; return a placeholder.
        return CostEstimate(notes="paid tool – no cost detail in manifest")
    return None


def validate_payload(schema: dict | None, payload: Any | None) -> tuple[bool, str | None]:
    """Validate the given payload against the provided JSON Schema.

    Returns (True, None) when valid, otherwise (False, error_message).
    """
    if schema is None:
        return True, None

    try:
        # jsonschema expects a concrete instance; use None -> {} for convenience
        instance = payload if payload is not None else {}
        jsonschema.validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as exc:
        return False, str(exc)
    except jsonschema.SchemaError as exc:
        return False, f"schema validation error: {exc}"
