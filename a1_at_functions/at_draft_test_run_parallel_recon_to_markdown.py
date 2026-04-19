# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_parallel_recon_to_markdown.py:7
# Component id: at.source.a1_at_functions.test_run_parallel_recon_to_markdown
from __future__ import annotations

__version__ = "0.1.0"

def test_run_parallel_recon_to_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    md = report.to_markdown()
    assert "# RECON_REPORT" in md
    assert "## Scout" in md
    assert "## Dependencies" in md
    assert "## Tier Distribution" in md
    assert "## Tests" in md
    assert "## Documentation" in md
