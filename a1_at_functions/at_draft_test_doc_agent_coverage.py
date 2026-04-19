# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:304
# Component id: at.source.ass_ade.test_doc_agent_coverage
__version__ = "0.1.0"

def test_doc_agent_coverage(tmp_path: Path) -> None:
    f = tmp_path / "module.py"
    f.write_text(
        'def good():\n    """Docs here."""\n    pass\n'
        "def bad():\n    pass\n",
        encoding="utf-8",
    )
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["doc_coverage"] == 0.5
    assert result["total_public_callables"] == 2
