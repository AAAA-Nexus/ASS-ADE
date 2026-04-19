# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_callback_on_skip.py:7
# Component id: at.source.a1_at_functions.test_callback_on_skip
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
