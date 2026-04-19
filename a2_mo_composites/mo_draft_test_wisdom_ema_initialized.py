# Extracted from C:/!ass-ade/tests/test_phase_engines.py:683
# Component id: mo.source.ass_ade.test_wisdom_ema_initialized
from __future__ import annotations

__version__ = "0.1.0"

def test_wisdom_ema_initialized(self):
    orch = self._make()
    assert orch._wisdom_ema == 0.5
