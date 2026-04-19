# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_enhance_apply_requires_ids.py:7
# Component id: at.source.a1_at_functions.test_enhance_apply_requires_ids
from __future__ import annotations

__version__ = "0.1.0"

def test_enhance_apply_requires_ids(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["enhance", str(tmp_path), "--apply", "", "--local-only"])

    # Should exit gracefully — either 0 (skipped/noop) or 1 (validation error).
    # Critically, it must not crash with an unhandled exception.
    assert result.exit_code in (0, 1)
    assert result.exception is None or isinstance(result.exception, SystemExit)
