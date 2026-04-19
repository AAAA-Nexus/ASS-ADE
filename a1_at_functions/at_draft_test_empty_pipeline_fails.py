# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_empty_pipeline_fails.py:7
# Component id: at.source.a1_at_functions.test_empty_pipeline_fails
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_pipeline_fails(self) -> None:
    pipe = Pipeline("empty")
    result = pipe.run()
    assert not result.passed
    assert len(result.steps) == 0
