# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_dev_starter.py:5
# Component id: at.source.ass_ade.test_dev_starter
__version__ = "0.1.0"

def test_dev_starter(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.dev_starter.return_value = StarterKit(project_name="my-project", x402_wired=True, files={})
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["dev", "starter", "my-project",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "my-project" in result.stdout
