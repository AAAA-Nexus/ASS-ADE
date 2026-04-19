# Extracted from C:/!ass-ade/tests/test_pipeline.py:232
# Component id: at.source.ass_ade.test_summary_failed
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
