# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_full_cycle_command_writes_report.py:5
# Component id: at.source.ass_ade.test_full_cycle_command_writes_report
__version__ = "0.1.0"

def test_full_cycle_command_writes_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    report_path = tmp_path / "reports" / "cycle.md"

    result = runner.invoke(
        app,
        [
            "cycle",
            "Enhance via cycle",
            "--path",
            str(tmp_path),
            "--report-out",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert report_path.exists()
    assert "ASS-ADE Public Enhancement Cycle" in report_path.read_text(encoding="utf-8")
