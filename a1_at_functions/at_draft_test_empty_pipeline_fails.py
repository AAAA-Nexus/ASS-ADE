# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:50
# Component id: at.source.ass_ade.test_empty_pipeline_fails
__version__ = "0.1.0"

    def test_empty_pipeline_fails(self) -> None:
        pipe = Pipeline("empty")
        result = pipe.run()
        assert not result.passed
        assert len(result.steps) == 0
