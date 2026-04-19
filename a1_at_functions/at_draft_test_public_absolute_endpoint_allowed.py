# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:16
# Component id: at.source.a1_at_functions.test_public_absolute_endpoint_allowed
from __future__ import annotations

__version__ = "0.1.0"

def test_public_absolute_endpoint_allowed(self) -> None:
    """Public absolute endpoints should be allowed (when domain resolves)."""
    # Use a well-known public domain that should resolve
    result = _validate_absolute_endpoint("https://cloudflare.com/api/tool")
    assert result == "https://cloudflare.com/api/tool"
