# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_remote_no_auth_required.py:7
# Component id: at.source.a1_at_functions.test_remote_no_auth_required
from __future__ import annotations

__version__ = "0.1.0"

def test_remote_no_auth_required(self) -> None:
    local = self._make_card("Local", skills=[("s1", "S1")])
    remote = self._make_card("Remote", skills=[("s1", "S1")])
    result = negotiate(local, remote)
    assert result.auth_compatible
