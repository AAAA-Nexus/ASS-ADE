# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:65
# Component id: at.source.ass_ade.test_non_https_absolute_rejected
from __future__ import annotations

__version__ = "0.1.0"

def test_non_https_absolute_rejected(self) -> None:
    """HTTP (non-HTTPS) absolute URLs should be rejected."""
    with pytest.raises(ValueError, match="https scheme"):
        _validate_absolute_endpoint("http://example.com/api")
