# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_initial_context_is_available.py:7
# Component id: at.source.a1_at_functions.test_initial_context_is_available
from __future__ import annotations

__version__ = "0.1.0"

def test_initial_context_is_available(self) -> None:
    pipe = Pipeline("initial")
    pipe.add("reader", context_reader)
    result = pipe.run({"message": "hello"})
    assert result.passed
    assert result.context["reader"]["read_message"] == "hello"
