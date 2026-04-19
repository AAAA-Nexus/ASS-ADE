# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:268
# Component id: at.source.ass_ade.test_writes_version_file
__version__ = "0.1.0"

    def test_writes_version_file(self, tmp_path: Path):
        tier_versions = {
            "a0_qk_constants": "0.1.0",
            "a1_at_functions": "0.2.3",
        }
        path = write_project_version_file(tmp_path, tier_versions, "20260418_120000")
        assert Path(path).name == "VERSION"
        lines = Path(path).read_text().splitlines()
        assert lines[0] == "0.2.3"
        assert "rebuild_tag=20260418_120000" in lines
