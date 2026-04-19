# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_custom_detail_message.py:7
# Component id: at.source.a1_at_functions.test_custom_detail_message
from __future__ import annotations

__version__ = "0.1.0"

def test_custom_detail_message(self) -> None:
    with pytest.raises(NexusServerError, match="oops"):
        raise_for_status(500, detail="oops")
