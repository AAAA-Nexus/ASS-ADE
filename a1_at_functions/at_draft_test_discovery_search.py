# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_discovery_search.py:5
# Component id: at.source.ass_ade.test_discovery_search
__version__ = "0.1.0"

def test_discovery_search(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.discovery_search.return_value = DiscoveryResult(agents=[], total=0)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["discovery", "search", "code review",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
