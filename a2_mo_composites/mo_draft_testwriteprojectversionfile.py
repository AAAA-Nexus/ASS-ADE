# Extracted from C:/!ass-ade/tests/test_version_tracker.py:267
# Component id: mo.source.ass_ade.testwriteprojectversionfile
from __future__ import annotations

__version__ = "0.1.0"

class TestWriteProjectVersionFile:
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

    def test_empty_tiers_returns_initial(self, tmp_path: Path):
        path = write_project_version_file(tmp_path, {}, "tag1")
        first_line = Path(path).read_text().splitlines()[0]
        assert first_line == INITIAL_VERSION
