# Extracted from C:/!ass-ade/tests/test_pipeline.py:72
# Component id: at.source.ass_ade.test_context_flows_through_steps
from __future__ import annotations

__version__ = "0.1.0"

def test_context_flows_through_steps(self) -> None:
    pipe = Pipeline("context")
    pipe.add("count1", counting_step)
    pipe.add("count2", counting_step)
    result = pipe.run()
    assert result.passed
    assert result.context["count"] == 2
