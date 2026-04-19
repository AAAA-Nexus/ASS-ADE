# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testprogresscallback.py:7
# Component id: mo.source.a2_mo_composites.testprogresscallback
from __future__ import annotations

__version__ = "0.1.0"

class TestProgressCallback:
    def test_callback_is_called(self) -> None:
        calls: list[tuple[str, StepStatus, int, int]] = []

        def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
            calls.append((name, status, current, total))

        pipe = Pipeline("prog", on_progress=on_progress)
        pipe.add("s1", pass_step)
        pipe.add("s2", pass_step)
        pipe.run()

        # Each step: RUNNING then PASSED = 2 calls per step = 4 total
        assert len(calls) == 4
        assert calls[0] == ("s1", StepStatus.RUNNING, 1, 2)
        assert calls[1] == ("s1", StepStatus.PASSED, 1, 2)
        assert calls[2] == ("s2", StepStatus.RUNNING, 2, 2)
        assert calls[3] == ("s2", StepStatus.PASSED, 2, 2)

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
