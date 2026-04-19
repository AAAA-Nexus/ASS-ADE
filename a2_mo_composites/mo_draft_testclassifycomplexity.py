# Extracted from C:/!ass-ade/tests/test_routing.py:15
# Component id: mo.source.ass_ade.testclassifycomplexity
from __future__ import annotations

__version__ = "0.1.0"

class TestClassifyComplexity:
    def test_simple_greeting(self):
        c = classify_complexity("Hello!")
        assert c < 0.3

    def test_code_request(self):
        c = classify_complexity("Write a Python function to sort a list")
        assert c >= 0.3  # code keywords

    def test_complex_multi_step(self):
        c = classify_complexity(
            "First, implement a REST API endpoint for user registration, "
            "then write integration tests and create a database migration"
        )
        assert c >= 0.5

    def test_formal_verification(self):
        c = classify_complexity(
            "Write a formal proof that this invariant holds across all states"
        )
        assert c >= 0.2  # formal keywords detected

    def test_long_text_adds_complexity(self):
        short = classify_complexity("Fix the bug")
        long_ = classify_complexity("Fix the bug " + "detailed context " * 100)
        assert long_ > short

    def test_range_bounded(self):
        c = classify_complexity(
            "First implement a function, then write a theorem proof, "
            "design the architecture, and create several test files " * 10
        )
        assert c <= 1.0

    def test_empty_string(self):
        assert classify_complexity("") == 0.0
