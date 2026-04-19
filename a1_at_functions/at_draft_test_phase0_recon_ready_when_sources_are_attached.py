# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_phase0_recon_ready_when_sources_are_attached.py:5
# Component id: at.source.ass_ade.test_phase0_recon_ready_when_sources_are_attached
__version__ = "0.1.0"

def test_phase0_recon_ready_when_sources_are_attached(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    result = phase0_recon(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
        provided_sources=["https://modelcontextprotocol.io/specification/2025-11-25/server/tools"],
    )

    assert result.verdict == "READY_FOR_PHASE_1"
    assert result.provided_sources
