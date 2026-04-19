# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_base_error_carries_context.py:7
# Component id: at.source.a1_at_functions.test_base_error_carries_context
from __future__ import annotations

__version__ = "0.1.0"

def test_base_error_carries_context(self) -> None:
    err = NexusError("boom", status_code=500, endpoint="/health", retry_after=2.5)
    assert err.detail == "boom"
    assert err.status_code == 500
    assert err.endpoint == "/health"
    assert err.retry_after == 2.5
    assert str(err) == "boom"
