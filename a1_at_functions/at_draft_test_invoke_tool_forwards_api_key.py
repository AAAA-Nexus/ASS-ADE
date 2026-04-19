# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_invoke_tool_forwards_api_key.py:7
# Component id: at.source.a1_at_functions.test_invoke_tool_forwards_api_key
from __future__ import annotations

__version__ = "0.1.0"

def test_invoke_tool_forwards_api_key() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("Authorization", "")
        captured["x_api_key"] = request.headers.get("X-API-Key", "")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    tool = MCPTool(name="paid-tool", endpoint="/paid", method="POST", paid=True)

    response = invoke_tool(
        "https://atomadic.tech",
        tool,
        {"probe": True},
        api_key="test-secret",
        transport=transport,
    )

    assert response.status_code == 200
    assert captured["authorization"] == "Bearer test-secret"
    assert captured["x_api_key"] == "test-secret"
