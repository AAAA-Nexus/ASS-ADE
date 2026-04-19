# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlocalagentcard.py:7
# Component id: mo.source.a2_mo_composites.testlocalagentcard
from __future__ import annotations

__version__ = "0.1.0"

class TestLocalAgentCard:
    def test_generates_valid_card(self, tmp_path: str) -> None:
        card = local_agent_card(str(tmp_path) if isinstance(tmp_path, type(None)) else ".")
        assert card.name == "ASS-ADE"
        assert card.provider is not None
        assert card.provider.organization == "Atomadic"
        assert len(card.skills) > 0

    def test_card_validates(self) -> None:
        card = local_agent_card(".")
        report = validate_agent_card(card.model_dump())
        # Should be valid (may have warnings but no errors)
        assert not report.errors
