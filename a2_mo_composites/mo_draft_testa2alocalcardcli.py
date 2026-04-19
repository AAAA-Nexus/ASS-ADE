# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testa2alocalcardcli.py:7
# Component id: mo.source.a2_mo_composites.testa2alocalcardcli
from __future__ import annotations

__version__ = "0.1.0"

class TestA2ALocalCardCLI:
    def test_local_card_displays(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card"])
        assert result.exit_code == 0
        assert "ASS-ADE" in result.stdout

    def test_local_card_json(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.stdout, strict=False)
        assert data["name"] == "ASS-ADE"
        assert "skills" in data
