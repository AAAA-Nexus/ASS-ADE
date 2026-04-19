# Extracted from C:/!ass-ade/tests/test_version_tracker.py:206
# Component id: qk.source.ass_ade.test_loads_from_manifest
from __future__ import annotations

__version__ = "0.1.0"

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
