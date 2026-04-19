# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nonexistent_path_returns_empty.py:7
# Component id: at.source.a1_at_functions.test_nonexistent_path_returns_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_nonexistent_path_returns_empty(self, tmp_path: Path):
    assert load_prev_versions(tmp_path / "nope.json") == {}
