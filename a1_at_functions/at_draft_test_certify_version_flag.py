# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_new_codebase_commands.py:124
# Component id: at.source.ass_ade.test_certify_version_flag
__version__ = "0.1.0"

def test_certify_version_flag(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(
        app,
        ["certify", str(tmp_path), "--version", "9.9.9", "--local-only"],
    )

    assert result.exit_code == 0
    cert_path = tmp_path / "CERTIFICATE.json"
    assert cert_path.exists()
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert["version"] == "9.9.9"
