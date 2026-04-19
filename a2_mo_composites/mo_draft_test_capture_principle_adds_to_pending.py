# Extracted from C:/!ass-ade/tests/test_phase_engines.py:427
# Component id: mo.source.ass_ade.test_capture_principle_adds_to_pending
from __future__ import annotations

__version__ = "0.1.0"

def test_capture_principle_adds_to_pending(self, tmp_path):
    fly = self._make(tmp_path)
    cid = fly.capture_principle("always verify before acting", confidence=0.9)
    assert cid != ""
    assert fly._pending[0].kind == "principle"
