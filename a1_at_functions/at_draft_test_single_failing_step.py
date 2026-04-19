# Extracted from C:/!ass-ade/tests/test_pipeline.py:64
# Component id: at.source.ass_ade.test_single_failing_step
from __future__ import annotations

__version__ = "0.1.0"

def test_single_failing_step(self) -> None:
    pipe = Pipeline("fail")
    pipe.add("step1", fail_step)
    result = pipe.run()
    assert not result.passed
    assert result.steps[0].status == StepStatus.FAILED
    assert result.steps[0].error == "something broke"
