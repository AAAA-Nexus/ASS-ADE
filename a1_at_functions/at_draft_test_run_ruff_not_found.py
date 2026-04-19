# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_ruff_not_found.py:7
# Component id: at.source.a1_at_functions.test_run_ruff_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_run_ruff_not_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Make shutil.which return None so run_ruff takes the early-exit path
    monkeypatch.setattr("ass_ade.local.linter.shutil.which", lambda _cmd: None)

    result = run_ruff(tmp_path)

    assert result.get("ok") is None
    assert "ruff not found" in result.get("error", "")
