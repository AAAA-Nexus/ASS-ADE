# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_capture_rejection_adds_negative.py:7
# Component id: at.source.a1_at_functions.test_capture_rejection_adds_negative
from __future__ import annotations

__version__ = "0.1.0"

def test_capture_rejection_adds_negative(self, tmp_path):
    fly = self._make(tmp_path)
    fly.capture_rejection("bad code", "A03_injection_eval")
    assert fly._pending[0].kind == "rejection"
