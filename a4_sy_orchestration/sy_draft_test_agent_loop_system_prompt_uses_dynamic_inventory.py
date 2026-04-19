# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_capabilities.py:35
# Component id: sy.source.ass_ade.test_agent_loop_system_prompt_uses_dynamic_inventory
__version__ = "0.1.0"

def test_agent_loop_system_prompt_uses_dynamic_inventory(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    prompt = build_system_prompt(str(tmp_path))

    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`read_file`" in prompt
    assert "Project type: Python" in prompt
