# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compute_codebase_digest_changes_on_file_edit.py:7
# Component id: at.source.a1_at_functions.test_compute_codebase_digest_changes_on_file_edit
from __future__ import annotations

__version__ = "0.1.0"

def test_compute_codebase_digest_changes_on_file_edit(tmp_path: Path) -> None:
    f = tmp_path / "mutable.py"
    f.write_text("version = 1\n", encoding="utf-8")

    r1 = compute_codebase_digest(tmp_path)

    f.write_text("version = 2\n", encoding="utf-8")

    r2 = compute_codebase_digest(tmp_path)

    assert r1["root_digest"] != r2["root_digest"]
