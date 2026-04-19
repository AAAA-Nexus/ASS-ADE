# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:259
# Component id: at.source.ass_ade.test_duration_tracking
__version__ = "0.1.0"

    def test_duration_tracking(self) -> None:
        pipe = Pipeline("dur")
        pipe.add("s1", pass_step)
        result = pipe.run()
        assert result.duration_ms >= 0
        assert result.steps[0].duration_ms >= 0
