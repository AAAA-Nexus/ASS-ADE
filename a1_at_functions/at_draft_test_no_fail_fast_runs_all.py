# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_no_fail_fast_runs_all.py:7
# Component id: at.source.a1_at_functions.test_no_fail_fast_runs_all
from __future__ import annotations

__version__ = "0.1.0"

def test_no_fail_fast_runs_all(self) -> None:
    pipe = Pipeline("noff", fail_fast=False)
    pipe.add("s1", pass_step)
    pipe.add("s2", fail_step)
    pipe.add("s3", pass_step)
    result = pipe.run()
    assert not result.passed
    assert result.steps[0].status == StepStatus.PASSED
    assert result.steps[1].status == StepStatus.FAILED
    assert result.steps[2].status == StepStatus.PASSED
