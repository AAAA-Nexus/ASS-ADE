# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_capabilities.py:16
# Component id: at.source.ass_ade.test_dynamic_prompt_includes_protocol_evolution_commands
__version__ = "0.1.0"

def test_dynamic_prompt_includes_protocol_evolution_commands(tmp_path: Path) -> None:
    prompt = build_atomadic_intent_prompt(tmp_path)

    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`protocol evolution-demo`" in prompt
    assert "`protocol version-bump`" in prompt
    assert "`prompt sync-agent`" in prompt
    assert "`prompt_hash`" in prompt
