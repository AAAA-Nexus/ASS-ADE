# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:361
# Component id: at.source.ass_ade.test_run_parallel_recon_to_dict
__version__ = "0.1.0"

def test_run_parallel_recon_to_dict(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    d = report.to_dict()
    assert "scout" in d
    assert "dependency" in d
    assert "tier" in d
    assert "test" in d
    assert "doc" in d
    assert "summary" in d
