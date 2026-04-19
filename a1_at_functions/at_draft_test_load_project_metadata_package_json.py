# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_load_project_metadata_package_json.py:7
# Component id: at.source.a1_at_functions.test_load_project_metadata_package_json
from __future__ import annotations

__version__ = "0.1.0"

def test_load_project_metadata_package_json(tmp_path: Path) -> None:
    pkg = tmp_path / "package.json"
    pkg.write_text(
        json.dumps({"name": "my-pkg", "version": "2.0.0", "description": "js package"}),
        encoding="utf-8",
    )

    meta = load_project_metadata(tmp_path)

    assert meta["name"] == "my-pkg"
    assert meta["version"] == "2.0.0"
