# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:52
# Component id: at.source.a1_at_functions.test_non_https_absolute_rejected
from __future__ import annotations

__version__ = "0.1.0"

def test_non_https_absolute_rejected(self) -> None:
    """HTTP (non-HTTPS) absolute URLs should be rejected."""
    with pytest.raises(ValueError, match="https scheme"):
        _validate_absolute_endpoint("http://example.com/api")
