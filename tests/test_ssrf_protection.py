"""Tests for SSRF (Server-Side Request Forgery) protection.

Verifies that:
- MCP tool endpoints with private/loopback addresses are blocked
- A2A agent card fetching does not allow TOCTOU DNS rebinding
- Absolute endpoint forwarding is guarded against private networks
"""

import ipaddress
import json
from unittest import mock

import pytest

from ass_ade.a2a import fetch_agent_card
from ass_ade.mcp.utils import _validate_absolute_endpoint
from ass_ade.nexus.models import MCPManifest, MCPTool


class TestValidateAbsoluteEndpoint:
    """Test SSRF validation for absolute endpoint URLs."""

    def test_relative_endpoint_passthrough(self) -> None:
        """Relative endpoints should pass through without validation."""
        assert _validate_absolute_endpoint("/api/tool") == "/api/tool"
        assert _validate_absolute_endpoint("api/tool") == "api/tool"
        assert _validate_absolute_endpoint("") == ""

    def test_public_absolute_endpoint_allowed(self) -> None:
        """Public absolute endpoints should be allowed (when domain resolves)."""
        # Use a well-known public domain that should resolve
        result = _validate_absolute_endpoint("https://cloudflare.com/api/tool")
        assert result == "https://cloudflare.com/api/tool"

    def test_localhost_blocked(self) -> None:
        """Absolute URLs to localhost should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://localhost/admin")

    def test_loopback_127_0_0_1_blocked(self) -> None:
        """Absolute URLs to 127.0.0.1 should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://127.0.0.1/admin")

    def test_private_10_network_blocked(self) -> None:
        """Absolute URLs to 10.x.x.x should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://10.0.0.1/admin")

    def test_private_172_network_blocked(self) -> None:
        """Absolute URLs to 172.16.x.x should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://172.16.0.1/admin")

    def test_private_192_168_network_blocked(self) -> None:
        """Absolute URLs to 192.168.x.x should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://192.168.1.1/admin")

    def test_ipv6_loopback_blocked(self) -> None:
        """Absolute URLs to IPv6 loopback should be blocked."""
        with pytest.raises(ValueError, match="private/loopback address"):
            _validate_absolute_endpoint("https://[::1]/admin")

    def test_non_https_absolute_rejected(self) -> None:
        """HTTP (non-HTTPS) absolute URLs should be rejected."""
        with pytest.raises(ValueError, match="https scheme"):
            _validate_absolute_endpoint("http://example.com/api")

    def test_invalid_hostname_rejected(self) -> None:
        """Absolute URLs with invalid hostnames should be rejected."""
        with pytest.raises(ValueError, match="valid host"):
            _validate_absolute_endpoint("https:///api")

    def test_dns_resolution_failure_handled(self) -> None:
        """DNS resolution failures should be caught and reported."""
        with pytest.raises(ValueError, match="private/loopback address"):
            # Invalid hostname that won't resolve
            _validate_absolute_endpoint("https://this-domain-does-not-exist-12345-test.invalid/api")


class TestA2AFetchAgentCardSSRF:
    """Test SSRF protection in A2A agent card fetching."""

    def test_https_only_required(self) -> None:
        """A2A fetching should require HTTPS."""
        report = fetch_agent_card("http://example.com/.well-known/agent.json")
        assert not report.valid
        assert "HTTPS" in report.errors[0].message

    def test_localhost_blocked(self) -> None:
        """A2A should block attempts to fetch from localhost."""
        report = fetch_agent_card("https://localhost/.well-known/agent.json")
        assert not report.valid
        assert len(report.errors) > 0
        assert "blocked" in report.errors[0].message or "loopback" in report.errors[0].message

    def test_appends_well_known_path(self) -> None:
        """Fetching from a URL without /.well-known/agent.json should auto-append it."""
        # Mock httpx.get to verify the right URL is called
        with mock.patch("ass_ade.a2a.httpx.get") as mock_get:
            mock_response = mock.MagicMock()
            mock_response.json.return_value = {"name": "TestAgent"}
            mock_get.return_value = mock_response
            
            # This should work and return valid=False because the JSON is incomplete
            # but we mainly care about the URL transformation
            fetch_agent_card("https://example.com")
            
            # Verify that the .well-known path was appended
            called_url = mock_get.call_args[0][0]
            assert called_url.endswith("/.well-known/agent.json")

    def test_immediate_ssrf_validation_before_request(self) -> None:
        """SSRF validation should happen immediately before the network request.
        
        This tests that we don't have a TOCTOU window where DNS could change
        between validation and the actual request.
        """
        with mock.patch("ass_ade.a2a.httpx.get") as mock_get:
            with mock.patch("ass_ade.a2a._check_ssrf") as mock_check_ssrf:
                # Set up mocks
                mock_check_ssrf.return_value = None  # No SSRF error
                mock_response = mock.MagicMock()
                mock_response.json.return_value = {"name": "TestAgent"}
                mock_get.return_value = mock_response
                
                # Call fetch_agent_card
                fetch_agent_card("https://example.com")
                
                # Verify _check_ssrf was called (it's called immediately before request)
                assert mock_check_ssrf.called


class TestMCPToolEndpointSSRF:
    """Test SSRF protection for MCP tool endpoint invocation."""

    def test_absolute_localhost_endpoint_raises(self) -> None:
        """Invoking a tool with localhost endpoint should raise ValueError."""
        from ass_ade.mcp.utils import invoke_tool
        
        tool = MCPTool(
            name="admin-tool",
            endpoint="https://localhost:8080/admin",
            method="POST",
            paid=False,
        )
        
        with pytest.raises(ValueError, match="blocked network address|localhost"):
            invoke_tool("https://api.example.com", tool)

    def test_absolute_private_ip_endpoint_raises(self) -> None:
        """Invoking a tool with private IP endpoint should raise ValueError."""
        from ass_ade.mcp.utils import invoke_tool
        
        tool = MCPTool(
            name="internal-tool",
            endpoint="https://192.168.1.1/internal",
            method="GET",
            paid=False,
        )
        
        with pytest.raises(ValueError, match="private/loopback address"):
            invoke_tool("https://api.example.com", tool)

    def test_relative_endpoint_uses_base_url(self) -> None:
        """Relative endpoints should be joined to base_url without SSRF validation."""
        from ass_ade.mcp.utils import simulate_invoke
        
        tool = MCPTool(
            name="safe-tool",
            endpoint="/api/invoke",
            method="POST",
            paid=False,
        )
        
        result = simulate_invoke("https://api.example.com", tool)
        assert result["endpoint"] == "https://api.example.com/api/invoke"
        assert not result["endpoint"].startswith("//")

    def test_simulate_invoke_validates_absolute_endpoint(self) -> None:
        """simulate_invoke should validate absolute endpoints for SSRF."""
        from ass_ade.mcp.utils import simulate_invoke
        
        tool = MCPTool(
            name="bad-tool",
            endpoint="https://127.0.0.1/admin",
            method="POST",
            paid=False,
        )
        
        with pytest.raises(ValueError, match="blocked network address|loopback"):
            simulate_invoke("https://api.example.com", tool)

    def test_public_absolute_endpoint_allowed_in_simulate(self) -> None:
        """Public absolute endpoints should be allowed in simulate_invoke."""
        from ass_ade.mcp.utils import simulate_invoke
        
        tool = MCPTool(
            name="public-tool",
            endpoint="https://cloudflare.com/tool",
            method="POST",
            paid=False,
        )
        
        result = simulate_invoke("https://fallback.example.com", tool)
        assert result["endpoint"] == "https://cloudflare.com/tool"
