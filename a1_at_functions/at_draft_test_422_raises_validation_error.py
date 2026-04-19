# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_422_raises_validation_error.py:7
# Component id: at.source.a1_at_functions.test_422_raises_validation_error
from __future__ import annotations

__version__ = "0.1.0"

def test_422_raises_validation_error(self) -> None:
    with pytest.raises(NexusValidationError):
        raise_for_status(422, detail="bad input")
