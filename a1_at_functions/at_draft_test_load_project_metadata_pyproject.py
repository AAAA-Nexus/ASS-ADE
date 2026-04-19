# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_load_project_metadata_pyproject.py:5
# Component id: at.source.ass_ade.test_load_project_metadata_pyproject
__version__ = "0.1.0"

def test_load_project_metadata_pyproject(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "myproject"\nversion = "1.2.3"\ndescription = "A test project"\n',
        encoding="utf-8",
    )

    meta = load_project_metadata(tmp_path)

    assert meta["name"] == "myproject"
    assert meta["version"] == "1.2.3"
    assert meta["description"] == "A test project"
