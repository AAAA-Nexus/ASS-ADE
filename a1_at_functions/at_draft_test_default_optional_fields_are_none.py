# Extracted from C:/!ass-ade/tests/test_errors.py:43
# Component id: at.source.ass_ade.test_default_optional_fields_are_none
from __future__ import annotations

__version__ = "0.1.0"

def test_default_optional_fields_are_none(self) -> None:
    err = NexusError("minimal")
    assert err.status_code is None
    assert err.endpoint is None
    assert err.retry_after is None
