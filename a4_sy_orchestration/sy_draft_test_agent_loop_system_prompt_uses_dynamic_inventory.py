# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_test_agent_loop_system_prompt_uses_dynamic_inventory.py:7
# Component id: sy.source.a4_sy_orchestration.test_agent_loop_system_prompt_uses_dynamic_inventory
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_loop_system_prompt_uses_dynamic_inventory(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    prompt = build_system_prompt(str(tmp_path))

    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`read_file`" in prompt
    assert "Project type: Python" in prompt
