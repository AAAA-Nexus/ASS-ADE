# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_chaining_add.py:7
# Component id: at.source.a1_at_functions.test_chaining_add
from __future__ import annotations

__version__ = "0.1.0"

def test_chaining_add(self) -> None:
    pipe = Pipeline("chain")
    returned = pipe.add("s1", pass_step).add("s2", pass_step)
    assert returned is pipe
    assert len(pipe.step_names) == 2
