# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testloadprevversions.py:7
# Component id: mo.source.a2_mo_composites.testloadprevversions
from __future__ import annotations

__version__ = "0.1.0"

class TestLoadPrevVersions:
    def test_none_path_returns_empty(self):
        assert load_prev_versions(None) == {}

    def test_nonexistent_path_returns_empty(self, tmp_path: Path):
        assert load_prev_versions(tmp_path / "nope.json") == {}

    def test_loads_from_manifest(self, tmp_path: Path):
        manifest = {
            "components": [
                {
                    "id": "at.foo",
                    "version": "0.2.1",
                    "body_hash": "abc123",
                    "body": "def foo(): pass",
                }
            ]
        }
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        result = load_prev_versions(p)
        assert "at.foo" in result
        assert result["at.foo"]["version"] == "0.2.1"
        assert result["at.foo"]["body_hash"] == "abc123"

    def test_missing_id_skipped(self, tmp_path: Path):
        manifest = {"components": [{"version": "0.1.0"}]}
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        assert load_prev_versions(p) == {}

    def test_invalid_json_returns_empty(self, tmp_path: Path):
        p = tmp_path / "MANIFEST.json"
        p.write_text("not json", encoding="utf-8")
        assert load_prev_versions(p) == {}
