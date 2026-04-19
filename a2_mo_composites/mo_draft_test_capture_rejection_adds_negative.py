# Extracted from C:/!ass-ade/tests/test_phase_engines.py:439
# Component id: mo.source.ass_ade.test_capture_rejection_adds_negative
from __future__ import annotations

__version__ = "0.1.0"

def test_capture_rejection_adds_negative(self, tmp_path):
    fly = self._make(tmp_path)
    fly.capture_rejection("bad code", "A03_injection_eval")
    assert fly._pending[0].kind == "rejection"
