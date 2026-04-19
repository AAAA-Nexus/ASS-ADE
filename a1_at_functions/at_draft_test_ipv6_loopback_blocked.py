# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:47
# Component id: at.source.a1_at_functions.test_ipv6_loopback_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_ipv6_loopback_blocked(self) -> None:
    """Absolute URLs to IPv6 loopback should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://[::1]/admin")
