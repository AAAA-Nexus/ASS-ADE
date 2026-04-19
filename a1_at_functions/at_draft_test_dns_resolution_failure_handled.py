# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:75
# Component id: at.source.ass_ade.test_dns_resolution_failure_handled
from __future__ import annotations

__version__ = "0.1.0"

def test_dns_resolution_failure_handled(self) -> None:
    """DNS resolution failures should be caught and reported."""
    with pytest.raises(ValueError, match="private/loopback address"):
        # Invalid hostname that won't resolve
        _validate_absolute_endpoint("https://this-domain-does-not-exist-12345-test.invalid/api")
