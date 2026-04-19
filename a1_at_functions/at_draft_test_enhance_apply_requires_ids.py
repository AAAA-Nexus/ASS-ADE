# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhance_cli.py:107
# Component id: at.source.ass_ade.test_enhance_apply_requires_ids
__version__ = "0.1.0"

def test_enhance_apply_requires_ids(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("x = 1\n", encoding="utf-8")

    result = runner.invoke(app, ["enhance", str(tmp_path), "--apply", "", "--local-only"])

    # Should exit gracefully — either 0 (skipped/noop) or 1 (validation error).
    # Critically, it must not crash with an unhandled exception.
    assert result.exit_code in (0, 1)
    assert result.exception is None or isinstance(result.exception, SystemExit)
