# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwritetierversionfile.py:7
# Component id: mo.source.a2_mo_composites.testwritetierversionfile
from __future__ import annotations

__version__ = "0.1.0"

class TestWriteTierVersionFile:
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
