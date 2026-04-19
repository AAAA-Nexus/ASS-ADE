# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:60
# Component id: at.source.ass_ade.test_ipv6_loopback_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_ipv6_loopback_blocked(self) -> None:
    """Absolute URLs to IPv6 loopback should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://[::1]/admin")
