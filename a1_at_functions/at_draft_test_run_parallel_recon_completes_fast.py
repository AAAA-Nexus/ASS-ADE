# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:333
# Component id: at.source.ass_ade.test_run_parallel_recon_completes_fast
__version__ = "0.1.0"

def test_run_parallel_recon_completes_fast(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    import time
    t0 = time.monotonic()
    run_parallel_recon(tmp_path)
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"Recon took {elapsed:.2f}s — exceeded 5s budget"
