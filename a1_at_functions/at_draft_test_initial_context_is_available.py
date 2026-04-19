# Extracted from C:/!ass-ade/tests/test_pipeline.py:80
# Component id: at.source.ass_ade.test_initial_context_is_available
from __future__ import annotations

__version__ = "0.1.0"

def test_initial_context_is_available(self) -> None:
    pipe = Pipeline("initial")
    pipe.add("reader", context_reader)
    result = pipe.run({"message": "hello"})
    assert result.passed
    assert result.context["reader"]["read_message"] == "hello"
