# Extracted from C:/!ass-ade/tests/test_phase_engines.py:139
# Component id: mo.source.ass_ade.test_refine_trigger_false_when_no_report
from __future__ import annotations

__version__ = "0.1.0"

def test_refine_trigger_false_when_no_report(self):
    loop = self._make_loop()
    assert loop._check_refine_trigger(None) is False
