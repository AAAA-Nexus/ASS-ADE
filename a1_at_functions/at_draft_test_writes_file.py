# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:239
# Component id: at.source.ass_ade.test_writes_file
__version__ = "0.1.0"

    def test_writes_file(self, tmp_path: Path):
        tier_dir = tmp_path / "a1_at_functions"
        tier_dir.mkdir()
        modules = [
            {"id": "at.foo", "name": "foo", "version": "0.1.0", "change_type": "new"},
            {"id": "at.bar", "name": "bar", "version": "0.2.0", "change_type": "minor"},
        ]
        path = write_tier_version_file(tier_dir, "a1_at_functions", modules)
        assert Path(path).exists()
        data = json.loads(Path(path).read_text())
        assert data["tier"] == "a1_at_functions"
        assert data["tier_version"] == "0.2.0"
        assert data["module_count"] == 2
