# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_context_packet_includes_file_hashes.py:5
# Component id: at.source.ass_ade.test_context_packet_includes_file_hashes
__version__ = "0.1.0"

def test_context_packet_includes_file_hashes(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    packet = build_context_packet(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
        file_paths=["src/mcp_server.py"],
        source_urls=["https://modelcontextprotocol.io/specification/2025-11-25/server/tools"],
    )

    assert packet.recon_verdict == "READY_FOR_PHASE_1"
    assert packet.files[0].path == "src/mcp_server.py"
    assert len(packet.files[0].sha256) == 64
