# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:70
# Component id: at.source.ass_ade.test_invalid_hostname_rejected
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_hostname_rejected(self) -> None:
    """Absolute URLs with invalid hostnames should be rejected."""
    with pytest.raises(ValueError, match="valid host"):
        _validate_absolute_endpoint("https:///api")
