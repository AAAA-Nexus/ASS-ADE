# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_returns_report.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_returns_report
from __future__ import annotations

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
