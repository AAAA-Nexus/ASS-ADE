# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_enhance_local_only.py:7
# Component id: at.source.a1_at_functions.test_enhance_local_only
from __future__ import annotations

__version__ = "0.1.0"

def test_enhance_local_only(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text(
        "def do_work():\n"
        "    try:\n"
        "        pass\n"
        "    except:\n"
        "        pass\n"
        "    # TODO: fix later\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["enhance", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    assert "findings" in result.output.lower() or "improvement" in result.output.lower()
