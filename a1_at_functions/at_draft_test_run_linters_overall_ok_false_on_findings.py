# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_run_linters_overall_ok_false_on_findings.py:5
# Component id: at.source.ass_ade.test_run_linters_overall_ok_false_on_findings
__version__ = "0.1.0"

def test_run_linters_overall_ok_false_on_findings(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
    (tmp_path / "bad.py").write_text("import os\n", encoding="utf-8")

    ruff_with_findings = {
        "linter": "ruff",
        "ok": False,
        "error_count": 5,
        "warning_count": 0,
        "findings": [{"file": "bad.py", "row": 1, "col": 1, "code": "F401", "message": "unused"}] * 5,
        "raw": "[]",
    }

    with (
        patch("ass_ade.local.linter.shutil.which", side_effect=lambda cmd: cmd if cmd == "ruff" else None),
        patch("ass_ade.local.linter.run_ruff", return_value=ruff_with_findings),
    ):
        result = run_linters(tmp_path)

    assert result["overall_ok"] is False
