# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_docs_engine.py:187
# Component id: mo.source.ass_ade.test_render_local_docs_writes_files
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
