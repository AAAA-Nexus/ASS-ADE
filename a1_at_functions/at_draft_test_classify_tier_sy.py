# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_classify_tier_sy.py:7
# Component id: at.source.a1_at_functions.test_classify_tier_sy
from __future__ import annotations

__version__ = "0.1.0"

def test_classify_tier_sy(tmp_path: Path) -> None:
    f = tmp_path / "app.py"
    f.write_text(
        "import os\nimport sys\nimport json\n"
        "def main(): pass\n"
        "if __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )
    assert _classify_tier(f) == "sy"
