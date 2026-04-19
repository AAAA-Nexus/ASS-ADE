# Extracted from C:/!ass-ade/tests/test_phase_engines.py:117
# Component id: mo.source.ass_ade.test_delegation_depth_resets_on_step
from __future__ import annotations

__version__ = "0.1.0"

def test_delegation_depth_resets_on_step(self):
    loop = self._make_loop()
    loop._delegation_depth = 10
    loop.reset_delegation_depth()
    assert loop.delegation_depth == 0
