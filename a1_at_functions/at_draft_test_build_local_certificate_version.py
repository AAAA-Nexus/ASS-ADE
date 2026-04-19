# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_certifier.py:105
# Component id: at.source.ass_ade.test_build_local_certificate_version
__version__ = "0.1.0"

def test_build_local_certificate_version(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path, version="1.2.3")

    assert cert["version"] == "1.2.3"
