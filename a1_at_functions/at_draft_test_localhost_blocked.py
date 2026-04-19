# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:35
# Component id: at.source.ass_ade.test_localhost_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_localhost_blocked(self) -> None:
    """Absolute URLs to localhost should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://localhost/admin")
