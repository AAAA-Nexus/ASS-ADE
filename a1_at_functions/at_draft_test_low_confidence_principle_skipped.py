# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_low_confidence_principle_skipped.py:7
# Component id: at.source.a1_at_functions.test_low_confidence_principle_skipped
from __future__ import annotations

__version__ = "0.1.0"

def test_low_confidence_principle_skipped(self, tmp_path):
    fly = self._make(tmp_path)
    cid = fly.capture_principle("weak idea", confidence=0.1)
    assert cid == ""
    assert len(fly._pending) == 0
