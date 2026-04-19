# Extracted from C:/!ass-ade/tests/test_recon_context.py:61
# Component id: at.source.ass_ade.test_phase0_recon_ready_when_sources_are_attached
from __future__ import annotations

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
