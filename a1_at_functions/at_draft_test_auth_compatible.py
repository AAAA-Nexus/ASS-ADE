# Extracted from C:/!ass-ade/tests/test_a2a.py:249
# Component id: at.source.ass_ade.test_auth_compatible
from __future__ import annotations

__version__ = "0.1.0"

def test_auth_compatible(self) -> None:
    local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["bearer"])
    remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
    result = negotiate(local, remote)
    assert result.compatible
    assert result.auth_compatible
