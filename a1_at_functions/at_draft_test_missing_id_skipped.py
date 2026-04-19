# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_missing_id_skipped.py:7
# Component id: at.source.a1_at_functions.test_missing_id_skipped
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_id_skipped(self, tmp_path: Path):
    manifest = {"components": [{"version": "0.1.0"}]}
    p = tmp_path / "MANIFEST.json"
    p.write_text(json.dumps(manifest), encoding="utf-8")
    assert load_prev_versions(p) == {}
