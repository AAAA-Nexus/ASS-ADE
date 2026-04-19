# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/utils.py:41
# Component id: sy.source.ass_ade.invoke_tool
__version__ = "0.1.0"

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
