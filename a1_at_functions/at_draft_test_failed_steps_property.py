# Extracted from C:/!ass-ade/tests/test_pipeline.py:247
# Component id: at.source.ass_ade.test_failed_steps_property
from __future__ import annotations

__version__ = "0.1.0"

def test_failed_steps_property(self) -> None:
    result = PipelineResult(
        name="test",
        steps=[
            StepResult(name="s1", status=StepStatus.PASSED),
            StepResult(name="s2", status=StepStatus.FAILED),
        ],
        passed=False,
    )
    assert len(result.failed_steps) == 1
    assert result.failed_steps[0].name == "s2"
