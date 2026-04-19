# Extracted from C:/!ass-ade/tests/test_new_codebase_commands.py:98
# Component id: at.source.ass_ade.test_certify_local_only
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_local_only(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def run(): pass\n", encoding="utf-8")

    result = runner.invoke(app, ["certify", str(tmp_path), "--local-only"])

    assert result.exit_code == 0
    cert_path = tmp_path / "CERTIFICATE.json"
    assert cert_path.exists(), "CERTIFICATE.json was not written"
