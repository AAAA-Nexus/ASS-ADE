# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_render_local_docs_writes_files.py:5
# Component id: at.source.ass_ade.test_render_local_docs_writes_files
__version__ = "0.1.0"

def test_render_local_docs_writes_files(tmp_path: Path) -> None:
    src_dir = tmp_path / "project"
    src_dir.mkdir()
    out_dir = tmp_path / "out"

    analysis = _minimal_analysis(src_dir)
    written = render_local_docs(analysis, out_dir)

    for name in _EXPECTED_FILES:
        assert name in written, f"{name} not in written dict"
        assert (out_dir / name).exists(), f"{name} not written to disk"
