# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:203
# Component id: at.source.ass_ade.test_nonexistent_path_returns_empty
__version__ = "0.1.0"

    def test_nonexistent_path_returns_empty(self, tmp_path: Path):
        assert load_prev_versions(tmp_path / "nope.json") == {}
