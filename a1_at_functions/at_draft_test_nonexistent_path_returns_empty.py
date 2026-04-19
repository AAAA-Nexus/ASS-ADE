# Extracted from C:/!ass-ade/tests/test_version_tracker.py:203
# Component id: at.source.ass_ade.test_nonexistent_path_returns_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_nonexistent_path_returns_empty(self, tmp_path: Path):
    assert load_prev_versions(tmp_path / "nope.json") == {}
