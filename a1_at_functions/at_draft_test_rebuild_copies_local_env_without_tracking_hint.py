# Extracted from C:/!ass-ade/tests/test_cli.py:214
# Component id: at.source.ass_ade.test_rebuild_copies_local_env_without_tracking_hint
from __future__ import annotations

__version__ = "0.1.0"

def test_rebuild_copies_local_env_without_tracking_hint(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    (src / ".env").write_text("AAAA_NEXUS_API_KEY=local-secret\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["env_handoff"] == str(out / ".env")
    assert (out / ".env").read_text(encoding="utf-8") == "AAAA_NEXUS_API_KEY=local-secret\n"
    assert ".env" in (out / ".gitignore").read_text(encoding="utf-8")
