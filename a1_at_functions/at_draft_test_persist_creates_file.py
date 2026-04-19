# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_persist_creates_file.py:7
# Component id: at.source.a1_at_functions.test_persist_creates_file
from __future__ import annotations

__version__ = "0.1.0"

def test_persist_creates_file(self, tmp_path: Path) -> None:
    pipe = Pipeline("persist", persist_dir=str(tmp_path))
    pipe.add("s1", pass_step)
    pipe.run()

    files = list(tmp_path.glob("persist_*.json"))
    assert len(files) == 1

    data = json.loads(files[0].read_text())
    assert data["name"] == "persist"
    assert data["passed"] is True
    assert len(data["steps"]) == 1
