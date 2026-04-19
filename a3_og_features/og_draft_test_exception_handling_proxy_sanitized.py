# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testsafeexecute.py:28
# Component id: og.source.a3_og_features.test_exception_handling_proxy_sanitized
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_handling_proxy_sanitized(self) -> None:
    """Exception in aegis_mcp_proxy should not leak raw exception to caller."""
    client = _mock_client()
    client.aegis_mcp_proxy.side_effect = TimeoutError("Request timed out after 30s")
    result = safe_execute(client, "slow_tool", "query", agent_id="agent-1")
    # Verify error is generic, not raw exception
    assert "error" in result.invocation_result
    assert result.invocation_result["error"] == "proxy_failed"
    assert "Request" not in result.invocation_result["error"]
    assert "timed out" not in result.invocation_result["error"]
    assert "30s" not in result.invocation_result["error"]
