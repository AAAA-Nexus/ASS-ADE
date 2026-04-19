# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:62
# Component id: at.source.a1_at_functions.test_dns_resolution_failure_handled
from __future__ import annotations

__version__ = "0.1.0"

def test_dns_resolution_failure_handled(self) -> None:
    """DNS resolution failures should be caught and reported."""
    with pytest.raises(ValueError, match="private/loopback address"):
        # Invalid hostname that won't resolve
        _validate_absolute_endpoint("https://this-domain-does-not-exist-12345-test.invalid/api")
