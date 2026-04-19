# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_certify_version_flag.py:7
# Component id: at.source.a1_at_functions.test_certify_version_flag
from __future__ import annotations

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
