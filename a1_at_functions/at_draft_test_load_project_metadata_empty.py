# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_load_project_metadata_empty.py:5
# Component id: at.source.ass_ade.test_load_project_metadata_empty
__version__ = "0.1.0"

def test_load_project_metadata_empty(tmp_path: Path) -> None:
    meta = load_project_metadata(tmp_path)

    assert isinstance(meta, dict)
    # Should return a dict with None values, not raise
    assert "name" in meta
