# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:50
# Component id: at.source.ass_ade.test_private_172_network_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_private_172_network_blocked(self) -> None:
    """Absolute URLs to 172.16.x.x should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://172.16.0.1/admin")
