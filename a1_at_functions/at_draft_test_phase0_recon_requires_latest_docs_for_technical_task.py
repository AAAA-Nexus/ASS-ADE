# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_phase0_recon_requires_latest_docs_for_technical_task.py:7
# Component id: at.source.a1_at_functions.test_phase0_recon_requires_latest_docs_for_technical_task
from __future__ import annotations

__version__ = "0.1.0"

def test_phase0_recon_requires_latest_docs_for_technical_task(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    result = phase0_recon(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
    )

    assert result.verdict == "RECON_REQUIRED"
    assert result.research_targets[0].suggested_url is not None
    assert "modelcontextprotocol.io" in result.research_targets[0].suggested_url
    assert "src/mcp_server.py" in result.codebase.relevant_files
