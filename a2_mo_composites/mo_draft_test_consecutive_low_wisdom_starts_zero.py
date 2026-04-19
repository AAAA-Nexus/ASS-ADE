# Extracted from C:/!ass-ade/tests/test_phase_engines.py:687
# Component id: mo.source.ass_ade.test_consecutive_low_wisdom_starts_zero
from __future__ import annotations

__version__ = "0.1.0"

def test_consecutive_low_wisdom_starts_zero(self):
    orch = self._make()
    assert orch._consecutive_low_wisdom == 0
