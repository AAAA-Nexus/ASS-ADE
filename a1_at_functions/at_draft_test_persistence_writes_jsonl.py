# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_persistence_writes_jsonl.py:7
# Component id: at.source.a1_at_functions.test_persistence_writes_jsonl
from __future__ import annotations

__version__ = "0.1.0"

def test_persistence_writes_jsonl(self, tmp_path: Path) -> None:
    state_file = tmp_path / "alerts.jsonl"
    b = BAS({"bas_state_path": str(state_file)})
    b.alert("novelty_spike", {"novelty": 0.8})
    assert state_file.exists()
    lines = [json.loads(line) for line in state_file.read_text().strip().splitlines()]
    assert lines[0]["kind"] == "novelty_spike"
