# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testfailfast.py:8
# Component id: sy.source.a2_mo_composites.test_fail_fast_skips_remaining
from __future__ import annotations

__version__ = "0.1.0"

def test_fail_fast_skips_remaining(self) -> None:
    pipe = Pipeline("ff", fail_fast=True)
    pipe.add("s1", pass_step)
    pipe.add("s2", fail_step)
    pipe.add("s3", pass_step)
    result = pipe.run()
    assert not result.passed
    assert result.steps[0].status == StepStatus.PASSED
    assert result.steps[1].status == StepStatus.FAILED
    assert result.steps[2].status == StepStatus.SKIPPED
