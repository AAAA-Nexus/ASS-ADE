# Extracted from C:/!ass-ade/tests/test_a2a.py:241
# Component id: at.source.ass_ade.test_auth_mismatch
from __future__ import annotations

__version__ = "0.1.0"

def test_auth_mismatch(self) -> None:
    local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["api_key"])
    remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
    result = negotiate(local, remote)
    assert not result.compatible
    assert not result.auth_compatible
    assert any("Auth mismatch" in n for n in result.notes)
