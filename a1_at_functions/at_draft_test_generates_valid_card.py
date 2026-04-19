# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_generates_valid_card.py:7
# Component id: at.source.a1_at_functions.test_generates_valid_card
from __future__ import annotations

__version__ = "0.1.0"

def test_generates_valid_card(self, tmp_path: str) -> None:
    card = local_agent_card(str(tmp_path) if isinstance(tmp_path, type(None)) else ".")
    assert card.name == "ASS-ADE"
    assert card.provider is not None
    assert card.provider.organization == "Atomadic"
    assert len(card.skills) > 0
