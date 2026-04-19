# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_test_invoke_tool_forwards_api_key.py:5
# Component id: at.source.ass_ade.test_invoke_tool_forwards_api_key
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
