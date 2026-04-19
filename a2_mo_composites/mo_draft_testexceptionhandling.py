# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testexceptionhandling.py:7
# Component id: mo.source.a2_mo_composites.testexceptionhandling
from __future__ import annotations

__version__ = "0.1.0"

class TestExceptionHandling:
    def test_exception_becomes_failed_step(self) -> None:
        pipe = Pipeline("err")
        pipe.add("boom", error_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[0].status == StepStatus.FAILED
        assert "kaboom" in result.steps[0].error

    def test_exception_with_fail_fast(self) -> None:
        pipe = Pipeline("errff", fail_fast=True)
        pipe.add("s1", pass_step)
        pipe.add("s2", error_step)
        pipe.add("s3", pass_step)
        result = pipe.run()
        assert not result.passed
        assert result.steps[2].status == StepStatus.SKIPPED
