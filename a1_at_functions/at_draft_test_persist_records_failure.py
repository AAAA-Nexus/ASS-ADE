# Extracted from C:/!ass-ade/tests/test_pipeline.py:197
# Component id: at.source.ass_ade.test_persist_records_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_persist_records_failure(self, tmp_path: Path) -> None:
    pipe = Pipeline("failp", persist_dir=str(tmp_path))
    pipe.add("s1", fail_step)
    pipe.run()

    files = list(tmp_path.glob("failp_*.json"))
    data = json.loads(files[0].read_text())
    assert data["passed"] is False
    assert data["steps"][0]["error"] == "something broke"
