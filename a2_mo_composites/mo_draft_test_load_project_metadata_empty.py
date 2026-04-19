# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_docs_engine.py:79
# Component id: mo.source.ass_ade.test_load_project_metadata_empty
__version__ = "0.1.0"

def test_load_project_metadata_empty(tmp_path: Path) -> None:
    meta = load_project_metadata(tmp_path)

    assert isinstance(meta, dict)
    # Should return a dict with None values, not raise
    assert "name" in meta
