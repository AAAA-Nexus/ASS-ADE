# Extracted from C:/!ass-ade/tests/test_pipeline.py:56
# Component id: at.source.ass_ade.test_single_passing_step
from __future__ import annotations

__version__ = "0.1.0"

def test_single_passing_step(self) -> None:
    pipe = Pipeline("single")
    pipe.add("step1", pass_step)
    result = pipe.run()
    assert result.passed
    assert len(result.steps) == 1
    assert result.steps[0].status == StepStatus.PASSED
