# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_classify_tier_qk.py:7
# Component id: at.source.a1_at_functions.test_classify_tier_qk
from __future__ import annotations

__version__ = "0.1.0"

def test_classify_tier_qk(tmp_path: Path) -> None:
    f = tmp_path / "constants.py"
    f.write_text("MAX = 3\nTIMEOUT = 30\n", encoding="utf-8")
    assert _classify_tier(f) == "qk"
