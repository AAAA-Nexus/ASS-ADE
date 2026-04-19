# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_certify_local_only.py:5
# Component id: at.source.ass_ade.test_certify_local_only
__version__ = "0.1.0"

def test_certify_local_only(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    cert_path = tmp_path / "CERTIFICATE.json"
    assert cert_path.exists(), "CERTIFICATE.json was not written"
