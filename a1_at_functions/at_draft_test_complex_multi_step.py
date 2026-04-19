# Extracted from C:/!ass-ade/tests/test_routing.py:24
# Component id: at.source.ass_ade.test_complex_multi_step
from __future__ import annotations

__version__ = "0.1.0"

def test_complex_multi_step(self):
    c = classify_complexity(
        "First, implement a REST API endpoint for user registration, "
        "then write integration tests and create a database migration"
    )
    assert c >= 0.5
