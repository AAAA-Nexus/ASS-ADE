# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_completes_fast.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_completes_fast
from __future__ import annotations

__version__ = "0.1.0"

def test_run_parallel_recon_completes_fast(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    import time
    t0 = time.monotonic()
    run_parallel_recon(tmp_path)
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"Recon took {elapsed:.2f}s — exceeded 5s budget"
