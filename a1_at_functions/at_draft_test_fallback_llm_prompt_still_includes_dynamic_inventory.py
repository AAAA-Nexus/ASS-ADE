# Extracted from C:/!ass-ade/tests/test_capabilities.py:61
# Component id: at.source.ass_ade.test_fallback_llm_prompt_still_includes_dynamic_inventory
from __future__ import annotations

__version__ = "0.1.0"

def test_fallback_llm_prompt_still_includes_dynamic_inventory(tmp_path: Path) -> None:
    prompt = interpreter._fallback_llm_system_prompt(tmp_path, "preferred_tone=direct")

    assert "preferred_tone=direct" in prompt
    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt
