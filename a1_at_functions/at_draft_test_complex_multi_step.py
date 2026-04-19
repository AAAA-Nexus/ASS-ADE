# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_complex_multi_step.py:7
# Component id: at.source.a1_at_functions.test_complex_multi_step
from __future__ import annotations

__version__ = "0.1.0"

def test_complex_multi_step(self):
    c = classify_complexity(
        "First, implement a REST API endpoint for user registration, "
        "then write integration tests and create a database migration"
    )
    assert c >= 0.5
