# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_linter.py:42
# Component id: at.source.ass_ade.test_run_ruff_not_found
__version__ = "0.1.0"

def test_run_ruff_not_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Make shutil.which return None so run_ruff takes the early-exit path
    monkeypatch.setattr("ass_ade.local.linter.shutil.which", lambda _cmd: None)

    result = run_ruff(tmp_path)

    assert result.get("ok") is None
    assert "ruff not found" in result.get("error", "")
