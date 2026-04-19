# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:60
# Component id: mo.source.a2_mo_composites.test_wisdom_ema_initialized
from __future__ import annotations

__version__ = "0.1.0"

def test_wisdom_ema_initialized(self):
    orch = self._make()
    assert orch._wisdom_ema == 0.5
