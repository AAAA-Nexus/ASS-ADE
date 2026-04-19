# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_empty_dir.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_empty_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_run_parallel_recon_empty_dir(tmp_path: Path) -> None:
    report = run_parallel_recon(tmp_path)
    assert report.scout["total_files"] == 0
    assert report.test["test_files"] == 0
    assert not report.doc["has_readme"]
