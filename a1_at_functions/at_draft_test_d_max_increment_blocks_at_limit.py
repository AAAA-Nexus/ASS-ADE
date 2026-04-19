# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_d_max_increment_blocks_at_limit.py:7
# Component id: at.source.a1_at_functions.test_d_max_increment_blocks_at_limit
from __future__ import annotations

__version__ = "0.1.0"

def test_d_max_increment_blocks_at_limit(self):
    from ass_ade.agent.loop import D_MAX
    loop = self._make_loop()
    # Set depth to D_MAX so the next increment exceeds it
    loop._delegation_depth = D_MAX
    assert loop.increment_delegation_depth() is False
