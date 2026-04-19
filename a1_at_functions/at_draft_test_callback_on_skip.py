# Extracted from C:/!ass-ade/tests/test_pipeline.py:165
# Component id: at.source.ass_ade.test_callback_on_skip
from __future__ import annotations

__version__ = "0.1.0"

def test_callback_on_skip(self) -> None:
    calls: list[tuple[str, StepStatus, int, int]] = []

    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        calls.append((name, status, current, total))

    pipe = Pipeline("skip", fail_fast=True, on_progress=on_progress)
    pipe.add("s1", fail_step)
    pipe.add("s2", pass_step)
    pipe.run()

    statuses = [s for _, s, _, _ in calls]
    assert StepStatus.SKIPPED in statuses
