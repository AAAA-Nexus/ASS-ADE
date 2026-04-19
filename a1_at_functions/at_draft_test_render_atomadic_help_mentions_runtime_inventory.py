# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_capabilities.py:46
# Component id: at.source.ass_ade.test_render_atomadic_help_mentions_runtime_inventory
__version__ = "0.1.0"

def test_render_atomadic_help_mentions_runtime_inventory(tmp_path: Path) -> None:
    help_text = render_atomadic_help(tmp_path)

    assert "runtime" in help_text
    assert "`protocol evolution-record`" in help_text
    assert "`context pack`" in help_text
