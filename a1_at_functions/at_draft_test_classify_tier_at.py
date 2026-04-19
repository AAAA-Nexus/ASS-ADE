# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:217
# Component id: at.source.ass_ade.test_classify_tier_at
from __future__ import annotations

__version__ = "0.1.0"

def test_classify_tier_at(tmp_path: Path) -> None:
    f = tmp_path / "utils.py"
    f.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    assert _classify_tier(f) == "at"
