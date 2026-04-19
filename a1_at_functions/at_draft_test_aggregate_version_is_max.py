# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwritetierversionfile.py:20
# Component id: at.source.ass_ade.test_aggregate_version_is_max
__version__ = "0.1.0"

    def test_aggregate_version_is_max(self, tmp_path: Path):
        tier_dir = tmp_path / "a2_mo_composites"
        tier_dir.mkdir()
        modules = [
            {"id": "mo.x", "name": "x", "version": "1.0.0", "change_type": "major"},
            {"id": "mo.y", "name": "y", "version": "0.5.0", "change_type": "minor"},
        ]
        path = write_tier_version_file(tier_dir, "a2_mo_composites", modules)
        data = json.loads(Path(path).read_text())
        assert data["tier_version"] == "1.0.0"
