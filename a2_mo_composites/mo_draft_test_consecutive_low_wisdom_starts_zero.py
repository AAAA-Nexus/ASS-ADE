# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:64
# Component id: mo.source.a2_mo_composites.test_consecutive_low_wisdom_starts_zero
from __future__ import annotations

__version__ = "0.1.0"

def test_consecutive_low_wisdom_starts_zero(self):
    orch = self._make()
    assert orch._consecutive_low_wisdom == 0
