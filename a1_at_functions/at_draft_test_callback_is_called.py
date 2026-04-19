# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:147
# Component id: at.source.ass_ade.test_callback_is_called
__version__ = "0.1.0"

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
