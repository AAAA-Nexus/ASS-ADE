# Extracted from C:/!ass-ade/tests/test_capabilities.py:17
# Component id: at.source.ass_ade.test_dynamic_prompt_includes_protocol_evolution_commands
from __future__ import annotations

__version__ = "0.1.0"

def test_dynamic_prompt_includes_protocol_evolution_commands(tmp_path: Path) -> None:
    prompt = build_atomadic_intent_prompt(tmp_path)

    assert "Dynamic Capability Inventory" in prompt
    assert "Capability summary" in prompt
    assert "Runtime routing rules" in prompt
    assert "Hosted Nexus MCP tools discovered in this session" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`protocol evolution-demo`" in prompt
    assert "`protocol version-bump`" in prompt
    assert "`prompt sync-agent`" in prompt
    assert "`prompt_hash`" in prompt
    assert "Generated at:" in prompt
