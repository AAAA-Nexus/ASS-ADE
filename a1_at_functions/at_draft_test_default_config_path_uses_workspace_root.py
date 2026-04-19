# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_default_config_path_uses_workspace_root.py:5
# Component id: at.source.ass_ade.test_default_config_path_uses_workspace_root
__version__ = "0.1.0"

def test_default_config_path_uses_workspace_root(tmp_path: Path) -> None:
    assert default_config_path(tmp_path) == tmp_path / ".ass-ade" / "config.json"
