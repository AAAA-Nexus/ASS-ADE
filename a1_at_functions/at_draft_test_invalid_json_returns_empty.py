# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:230
# Component id: at.source.ass_ade.test_invalid_json_returns_empty
__version__ = "0.1.0"

    def test_invalid_json_returns_empty(self, tmp_path: Path):
        p = tmp_path / "MANIFEST.json"
        p.write_text("not json", encoding="utf-8")
        assert load_prev_versions(p) == {}
