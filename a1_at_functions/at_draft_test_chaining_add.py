# Extracted from C:/!ass-ade/tests/test_pipeline.py:87
# Component id: at.source.ass_ade.test_chaining_add
from __future__ import annotations

__version__ = "0.1.0"

def test_chaining_add(self) -> None:
    pipe = Pipeline("chain")
    returned = pipe.add("s1", pass_step).add("s2", pass_step)
    assert returned is pipe
    assert len(pipe.step_names) == 2
