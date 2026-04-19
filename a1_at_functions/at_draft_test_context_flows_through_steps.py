# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_context_flows_through_steps.py:7
# Component id: at.source.a1_at_functions.test_context_flows_through_steps
from __future__ import annotations

__version__ = "0.1.0"

def test_context_flows_through_steps(self) -> None:
    pipe = Pipeline("context")
    pipe.add("count1", counting_step)
    pipe.add("count2", counting_step)
    result = pipe.run()
    assert result.passed
    assert result.context["count"] == 2
