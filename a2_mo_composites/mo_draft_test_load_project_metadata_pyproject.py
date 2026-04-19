# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_docs_engine.py:52
# Component id: mo.source.ass_ade.test_load_project_metadata_pyproject
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
