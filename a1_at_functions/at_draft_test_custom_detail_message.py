# Extracted from C:/!ass-ade/tests/test_errors.py:89
# Component id: at.source.ass_ade.test_custom_detail_message
from __future__ import annotations

__version__ = "0.1.0"

def test_custom_detail_message(self) -> None:
    with pytest.raises(NexusServerError, match="oops"):
        raise_for_status(500, detail="oops")
