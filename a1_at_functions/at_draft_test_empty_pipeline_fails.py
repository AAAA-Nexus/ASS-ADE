# Extracted from C:/!ass-ade/tests/test_pipeline.py:50
# Component id: at.source.ass_ade.test_empty_pipeline_fails
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_pipeline_fails(self) -> None:
    pipe = Pipeline("empty")
    result = pipe.run()
    assert not result.passed
    assert len(result.steps) == 0
