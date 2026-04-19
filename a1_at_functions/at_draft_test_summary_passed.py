# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_summary_passed.py:7
# Component id: at.source.a1_at_functions.test_summary_passed
from __future__ import annotations

__version__ = "0.1.0"

def test_summary_passed(self) -> None:
    result = PipelineResult(
        name="test",
        steps=[
            StepResult(name="s1", status=StepStatus.PASSED),
            StepResult(name="s2", status=StepStatus.PASSED),
        ],
        passed=True,
        duration_ms=150.0,
    )
    assert "[PASSED]" in result.summary
    assert "2/2 passed" in result.summary
