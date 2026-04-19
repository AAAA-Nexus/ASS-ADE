# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:40
# Component id: at.source.ass_ade.test_loopback_127_0_0_1_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_loopback_127_0_0_1_blocked(self) -> None:
    """Absolute URLs to 127.0.0.1 should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://127.0.0.1/admin")
