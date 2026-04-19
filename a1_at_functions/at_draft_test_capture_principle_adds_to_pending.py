# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_capture_principle_adds_to_pending.py:7
# Component id: at.source.a1_at_functions.test_capture_principle_adds_to_pending
from __future__ import annotations

__version__ = "0.1.0"

def test_capture_principle_adds_to_pending(self, tmp_path):
    fly = self._make(tmp_path)
    cid = fly.capture_principle("always verify before acting", confidence=0.9)
    assert cid != ""
    assert fly._pending[0].kind == "principle"
