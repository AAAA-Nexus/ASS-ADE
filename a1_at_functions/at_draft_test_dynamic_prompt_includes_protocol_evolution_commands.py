# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_dynamic_prompt_includes_protocol_evolution_commands.py:7
# Component id: at.source.a1_at_functions.test_dynamic_prompt_includes_protocol_evolution_commands
from __future__ import annotations

__version__ = "0.1.0"

def test_dynamic_prompt_includes_protocol_evolution_commands(tmp_path: Path) -> None:
    prompt = build_atomadic_intent_prompt(tmp_path)

    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`protocol evolution-demo`" in prompt
    assert "`protocol version-bump`" in prompt
    assert "`prompt sync-agent`" in prompt
    assert "`prompt_hash`" in prompt
