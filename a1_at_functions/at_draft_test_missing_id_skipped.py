# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:224
# Component id: at.source.ass_ade.test_missing_id_skipped
__version__ = "0.1.0"

    def test_missing_id_skipped(self, tmp_path: Path):
        manifest = {"components": [{"version": "0.1.0"}]}
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        assert load_prev_versions(p) == {}
