# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_duration_tracking.py:7
# Component id: at.source.a1_at_functions.test_duration_tracking
from __future__ import annotations

__version__ = "0.1.0"

def test_duration_tracking(self) -> None:
    pipe = Pipeline("dur")
    pipe.add("s1", pass_step)
    result = pipe.run()
    assert result.duration_ms >= 0
    assert result.steps[0].duration_ms >= 0
