# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testsafeexecute.py:38
# Component id: og.source.ass_ade.test_exception_handling_proxy_network_error_sanitized
__version__ = "0.1.0"

    def test_exception_handling_proxy_network_error_sanitized(self) -> None:
        """Network errors should be sanitized."""
        client = _mock_client()
        client.aegis_mcp_proxy.side_effect = ConnectionError("Failed to connect to 192.168.1.1:8080")
        result = safe_execute(client, "network_tool", "", agent_id="agent-2")
        assert result.invocation_result["error"] == "proxy_failed"
        assert "192.168.1.1" not in result.invocation_result["error"]
        assert "Failed" not in result.invocation_result["error"]
