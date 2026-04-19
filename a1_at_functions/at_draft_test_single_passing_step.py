# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_single_passing_step.py:7
# Component id: at.source.a1_at_functions.test_single_passing_step
from __future__ import annotations

__version__ = "0.1.0"

def test_single_passing_step(self) -> None:
    pipe = Pipeline("single")
    pipe.add("step1", pass_step)
    result = pipe.run()
    assert result.passed
    assert len(result.steps) == 1
    assert result.steps[0].status == StepStatus.PASSED
