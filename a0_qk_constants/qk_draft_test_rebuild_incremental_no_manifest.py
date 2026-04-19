# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:213
# Component id: qk.source.ass_ade.test_rebuild_incremental_no_manifest
__version__ = "0.1.0"

def test_rebuild_incremental_no_manifest(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def foo(): pass\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(
        app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--incremental"]
    )

    assert result.exit_code == 0
