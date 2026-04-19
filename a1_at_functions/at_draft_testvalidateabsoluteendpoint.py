# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:20
# Component id: at.source.ass_ade.testvalidateabsoluteendpoint
from __future__ import annotations

__version__ = "0.1.0"

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
