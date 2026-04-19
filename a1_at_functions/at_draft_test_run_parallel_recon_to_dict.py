# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_to_dict.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_to_dict
from __future__ import annotations

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
