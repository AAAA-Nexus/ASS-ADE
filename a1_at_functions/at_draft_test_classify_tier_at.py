# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_classify_tier_at.py:7
# Component id: at.source.a1_at_functions.test_classify_tier_at
from __future__ import annotations

__version__ = "0.1.0"

def test_classify_tier_at(tmp_path: Path) -> None:
    f = tmp_path / "utils.py"
    f.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    assert _classify_tier(f) == "at"
