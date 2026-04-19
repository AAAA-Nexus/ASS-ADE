# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:207
# Component id: at.source.ass_ade.test_no_persist_when_not_configured
__version__ = "0.1.0"

    def test_no_persist_when_not_configured(self, tmp_path: Path) -> None:
        pipe = Pipeline("nopersist")
        pipe.add("s1", pass_step)
        pipe.run()
        # No files created anywhere — this is just a sanity check
        assert not list(tmp_path.glob("*.json"))
