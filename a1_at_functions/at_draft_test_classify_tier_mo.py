# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_classify_tier_mo.py:7
# Component id: at.source.a1_at_functions.test_classify_tier_mo
from __future__ import annotations

__version__ = "0.1.0"

def test_classify_tier_mo(tmp_path: Path) -> None:
    f = tmp_path / "session.py"
    f.write_text(
        "class Session:\n"
        "    def __init__(self, uid):\n"
        "        self.uid = uid\n",
        encoding="utf-8",
    )
    assert _classify_tier(f) == "mo"
