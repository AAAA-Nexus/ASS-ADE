# Extracted from C:/!ass-ade/tests/test_capabilities.py:52
# Component id: at.source.ass_ade.test_render_atomadic_help_mentions_runtime_inventory
from __future__ import annotations

__version__ = "0.1.0"

def test_render_atomadic_help_mentions_runtime_inventory(tmp_path: Path) -> None:
    help_text = render_atomadic_help(tmp_path)

    assert "runtime" in help_text
    assert "Capability counts" in help_text
    assert "`protocol evolution-record`" in help_text
    assert "`context pack`" in help_text
