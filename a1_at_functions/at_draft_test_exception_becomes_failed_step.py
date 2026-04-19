# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_exception_becomes_failed_step.py:7
# Component id: at.source.a1_at_functions.test_exception_becomes_failed_step
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_becomes_failed_step(self) -> None:
    pipe = Pipeline("err")
    pipe.add("boom", error_step)
    result = pipe.run()
    assert not result.passed
    assert result.steps[0].status == StepStatus.FAILED
    assert "kaboom" in result.steps[0].error
