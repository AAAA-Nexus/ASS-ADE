# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_persistence_io_error_does_not_crash.py:7
# Component id: at.source.a1_at_functions.test_persistence_io_error_does_not_crash
from __future__ import annotations

__version__ = "0.1.0"

def test_persistence_io_error_does_not_crash(self, tmp_path: Path) -> None:
    # Point to a directory path (not writable as file)
    b = BAS({"bas_state_path": str(tmp_path)})
    b.alert("novelty_spike", {"novelty": 0.8})  # should not raise
