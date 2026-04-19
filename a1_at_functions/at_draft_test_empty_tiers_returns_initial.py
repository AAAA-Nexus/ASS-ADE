# Extracted from C:/!ass-ade/tests/test_version_tracker.py:279
# Component id: at.source.ass_ade.test_empty_tiers_returns_initial
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_tiers_returns_initial(self, tmp_path: Path):
    path = write_project_version_file(tmp_path, {}, "tag1")
    first_line = Path(path).read_text().splitlines()[0]
    assert first_line == INITIAL_VERSION
