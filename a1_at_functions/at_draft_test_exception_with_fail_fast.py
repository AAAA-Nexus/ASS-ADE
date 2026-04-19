# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_exception_with_fail_fast.py:7
# Component id: at.source.a1_at_functions.test_exception_with_fail_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_with_fail_fast(self) -> None:
    pipe = Pipeline("errff", fail_fast=True)
    pipe.add("s1", pass_step)
    pipe.add("s2", error_step)
    pipe.add("s3", pass_step)
    result = pipe.run()
    assert not result.passed
    assert result.steps[2].status == StepStatus.SKIPPED
