# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_delegation_depth_resets_on_step.py:7
# Component id: at.source.a1_at_functions.test_delegation_depth_resets_on_step
from __future__ import annotations

__version__ = "0.1.0"

def test_delegation_depth_resets_on_step(self):
    loop = self._make_loop()
    loop._delegation_depth = 10
    loop.reset_delegation_depth()
    assert loop.delegation_depth == 0
