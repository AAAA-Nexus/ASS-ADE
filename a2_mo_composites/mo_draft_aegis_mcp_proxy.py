# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:736
# Component id: mo.source.ass_ade.aegis_mcp_proxy
from __future__ import annotations

__version__ = "0.1.0"

def aegis_mcp_proxy(
    self,
    tool: str | None = None,
    tool_input: str = "",
    agent_id: str | None = None,
    *,
    tool_name: str | None = None,
    payload: dict[str, Any] | None = None,
    **kwargs: Any,
) -> AegisProxyResult:
    """/v1/aegis/mcp-proxy/execute — MCP tool-call firewall (AEG-100). $0.040/call"""
    resolved_tool = tool or tool_name or ""
    resolved_tool_input = tool_input
    if payload is not None and not resolved_tool_input:
        resolved_tool_input = json.dumps(payload)
    body: dict[str, Any] = {"tool": resolved_tool, "tool_input": resolved_tool_input, **kwargs}
    if agent_id:
        body["agent_id"] = agent_id
    return self._post_model("/v1/aegis/mcp-proxy/execute", AegisProxyResult, body)
