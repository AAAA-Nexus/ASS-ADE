# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp.py:110
# Component id: sy.source.ass_ade.handler
__version__ = "0.1.0"

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("Authorization", "")
        captured["x_api_key"] = request.headers.get("X-API-Key", "")
        return httpx.Response(200, json={"ok": True})
