# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_unknown_4xx_raises_base_error.py:7
# Component id: at.source.a1_at_functions.test_unknown_4xx_raises_base_error
from __future__ import annotations

__version__ = "0.1.0"

def test_unknown_4xx_raises_base_error(self) -> None:
    with pytest.raises(NexusError) as exc_info:
        raise_for_status(418)
    assert exc_info.value.status_code == 418
