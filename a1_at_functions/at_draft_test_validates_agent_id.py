# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:47
# Component id: at.source.a3_og_features.test_validates_agent_id
from __future__ import annotations

__version__ = "0.1.0"

def test_validates_agent_id(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        trust_gate(_mock_client(), "")
