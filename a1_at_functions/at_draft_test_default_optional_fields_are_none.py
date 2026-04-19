# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_default_optional_fields_are_none.py:7
# Component id: at.source.a1_at_functions.test_default_optional_fields_are_none
from __future__ import annotations

__version__ = "0.1.0"

def test_default_optional_fields_are_none(self) -> None:
    err = NexusError("minimal")
    assert err.status_code is None
    assert err.endpoint is None
    assert err.retry_after is None
