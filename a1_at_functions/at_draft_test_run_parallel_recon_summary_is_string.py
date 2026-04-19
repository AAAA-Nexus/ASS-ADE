# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_summary_is_string.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_summary_is_string
from __future__ import annotations

__version__ = "0.1.0"

def test_run_parallel_recon_summary_is_string(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    assert isinstance(report.summary, str)
    assert len(report.summary) > 20
