# Extracted from C:/!ass-ade/tests/test_certifier.py:67
# Component id: at.source.ass_ade.test_compute_codebase_digest_deterministic
from __future__ import annotations

__version__ = "0.1.0"

def test_compute_codebase_digest_deterministic(tmp_path: Path) -> None:
    (tmp_path / "stable.py").write_text("stable = True\n", encoding="utf-8")

    r1 = compute_codebase_digest(tmp_path)
    r2 = compute_codebase_digest(tmp_path)

    assert r1["root_digest"] == r2["root_digest"]
