# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_full_cycle_command_writes_json_report.py:5
# Component id: at.source.ass_ade.test_full_cycle_command_writes_json_report
__version__ = "0.1.0"

def test_full_cycle_command_writes_json_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    json_report_path = tmp_path / "reports" / "cycle.json"

    result = runner.invoke(
        app,
        [
            "cycle",
            "Enhance via cycle",
            "--path",
            str(tmp_path),
            "--json-out",
            str(json_report_path),
        ],
    )

    assert result.exit_code == 0
    assert json_report_path.exists()
    payload = json.loads(json_report_path.read_text(encoding="utf-8"))
    assert payload["goal"] == "Enhance via cycle"
    assert "report" in payload
