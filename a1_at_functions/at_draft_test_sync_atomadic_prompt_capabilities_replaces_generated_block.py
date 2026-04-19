# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_sync_atomadic_prompt_capabilities_replaces_generated_block.py:5
# Component id: at.source.ass_ade.test_sync_atomadic_prompt_capabilities_replaces_generated_block
__version__ = "0.1.0"

def test_sync_atomadic_prompt_capabilities_replaces_generated_block(tmp_path: Path) -> None:
    prompt_path = tmp_path / "agents" / "atomadic_interpreter.md"
    prompt_path.parent.mkdir()
    prompt_path.write_text(
        "# Atomadic\n\n---\n\n## Current Capabilities\n\nold stale block\n",
        encoding="utf-8",
    )

    result = sync_atomadic_prompt_capabilities(repo_root=tmp_path, prompt_path=prompt_path)

    assert result == prompt_path
    text = prompt_path.read_text(encoding="utf-8")
    assert "old stale block" not in text
    assert "`protocol evolution-record`" in text
    assert "`prompt sync-agent`" in text
