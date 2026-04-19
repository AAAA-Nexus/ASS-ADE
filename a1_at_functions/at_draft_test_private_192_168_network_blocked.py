# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:55
# Component id: at.source.ass_ade.test_private_192_168_network_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_private_192_168_network_blocked(self) -> None:
    """Absolute URLs to 192.168.x.x should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://192.168.1.1/admin")
