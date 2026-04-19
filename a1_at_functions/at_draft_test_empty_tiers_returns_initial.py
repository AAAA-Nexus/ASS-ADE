# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_empty_tiers_returns_initial.py:7
# Component id: at.source.a1_at_functions.test_empty_tiers_returns_initial
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_tiers_returns_initial(self, tmp_path: Path):
    path = write_project_version_file(tmp_path, {}, "tag1")
    first_line = Path(path).read_text().splitlines()[0]
    assert first_line == INITIAL_VERSION
