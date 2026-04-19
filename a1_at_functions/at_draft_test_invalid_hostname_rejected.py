# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:57
# Component id: at.source.a1_at_functions.test_invalid_hostname_rejected
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_hostname_rejected(self) -> None:
    """Absolute URLs with invalid hostnames should be rejected."""
    with pytest.raises(ValueError, match="valid host"):
        _validate_absolute_endpoint("https:///api")
