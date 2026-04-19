# Extracted from C:/!ass-ade/tests/test_errors.py:20
# Component id: at.source.ass_ade.test_base_error_carries_context
from __future__ import annotations

__version__ = "0.1.0"

def test_base_error_carries_context(self) -> None:
    err = NexusError("boom", status_code=500, endpoint="/health", retry_after=2.5)
    assert err.detail == "boom"
    assert err.status_code == 500
    assert err.endpoint == "/health"
    assert err.retry_after == 2.5
    assert str(err) == "boom"
