# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:42
# Component id: at.source.a1_at_functions.test_private_192_168_network_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_private_192_168_network_blocked(self) -> None:
    """Absolute URLs to 192.168.x.x should be blocked."""
    with pytest.raises(ValueError, match="private/loopback address"):
        _validate_absolute_endpoint("https://192.168.1.1/admin")
