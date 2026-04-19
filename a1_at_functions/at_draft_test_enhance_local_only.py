# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhance_cli.py:45
# Component id: at.source.ass_ade.test_enhance_local_only
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
