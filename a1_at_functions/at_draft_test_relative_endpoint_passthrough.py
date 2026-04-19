# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:23
# Component id: at.source.ass_ade.test_relative_endpoint_passthrough
from __future__ import annotations

__version__ = "0.1.0"

def test_relative_endpoint_passthrough(self) -> None:
    """Relative endpoints should pass through without validation."""
    assert _validate_absolute_endpoint("/api/tool") == "/api/tool"
    assert _validate_absolute_endpoint("api/tool") == "api/tool"
    assert _validate_absolute_endpoint("") == ""
