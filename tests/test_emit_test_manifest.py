from __future__ import annotations

from pathlib import Path

from ass_ade.a3_og_features.emit_test_manifest import run_emit_test_manifest


def test_emit_test_manifest_writes_file(repo_root: Path) -> None:
    out = run_emit_test_manifest(repo_root)
    p = Path(out["written"])
    assert p.is_file()
    assert p.name == "_qualnames.json"
    assert out["bytes"] > 10
