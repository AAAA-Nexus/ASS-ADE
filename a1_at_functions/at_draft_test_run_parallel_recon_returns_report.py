# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:320
# Component id: at.source.ass_ade.test_run_parallel_recon_returns_report
__version__ = "0.1.0"

def test_run_parallel_recon_returns_report(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)

    assert isinstance(report, ReconReport)
    assert report.root == str(tmp_path)
    assert report.duration_ms >= 0
    assert report.scout["total_files"] > 0
    assert isinstance(report.recommendations, list)
    assert len(report.recommendations) > 0
    assert report.next_action
