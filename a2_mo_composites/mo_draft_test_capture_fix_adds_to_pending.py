# Extracted from C:/!ass-ade/tests/test_phase_engines.py:420
# Component id: mo.source.ass_ade.test_capture_fix_adds_to_pending
from __future__ import annotations

__version__ = "0.1.0"

def test_capture_fix_adds_to_pending(self, tmp_path):
    fly = self._make(tmp_path)
    cid = fly.capture_fix("old code", "new code")
    assert cid != ""
    assert len(fly._pending) == 1
    assert fly._pending[0].kind == "fix"
