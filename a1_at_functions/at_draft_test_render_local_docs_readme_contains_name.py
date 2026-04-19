# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_render_local_docs_readme_contains_name.py:5
# Component id: at.source.ass_ade.test_render_local_docs_readme_contains_name
__version__ = "0.1.0"

def test_render_local_docs_readme_contains_name(tmp_path: Path) -> None:
    src_dir = tmp_path / "project"
    src_dir.mkdir()
    out_dir = tmp_path / "out"

    analysis = _minimal_analysis(src_dir)
    render_local_docs(analysis, out_dir)

    readme = (out_dir / "README.md").read_text(encoding="utf-8")
    assert "testpkg" in readme
