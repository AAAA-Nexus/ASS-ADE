# Extracted from C:/!ass-ade/tests/test_errors.py:69
# Component id: at.source.ass_ade.test_422_raises_validation_error
from __future__ import annotations

__version__ = "0.1.0"

def test_422_raises_validation_error(self) -> None:
    with pytest.raises(NexusValidationError):
        raise_for_status(422, detail="bad input")
