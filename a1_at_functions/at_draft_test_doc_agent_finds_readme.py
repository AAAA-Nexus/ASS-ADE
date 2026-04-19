# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:290
# Component id: at.source.ass_ade.test_doc_agent_finds_readme
__version__ = "0.1.0"

def test_doc_agent_finds_readme(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["has_readme"] is True
