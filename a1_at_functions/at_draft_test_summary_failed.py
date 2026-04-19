# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_summary_failed.py:7
# Component id: at.source.a1_at_functions.test_summary_failed
from __future__ import annotations

__version__ = "0.1.0"

def test_summary_failed(self) -> None:
    result = PipelineResult(
        name="test",
        steps=[
            StepResult(name="s1", status=StepStatus.PASSED),
            StepResult(name="s2", status=StepStatus.FAILED, error="x"),
            StepResult(name="s3", status=StepStatus.SKIPPED),
        ],
        passed=False,
        duration_ms=200.0,
    )
    assert "[FAILED]" in result.summary
    assert "1 failed" in result.summary
    assert "1 skipped" in result.summary
