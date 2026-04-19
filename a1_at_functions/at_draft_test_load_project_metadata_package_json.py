# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_load_project_metadata_package_json.py:5
# Component id: at.source.ass_ade.test_load_project_metadata_package_json
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
