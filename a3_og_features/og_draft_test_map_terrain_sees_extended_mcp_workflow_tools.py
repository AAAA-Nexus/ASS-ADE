# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_test_map_terrain_sees_extended_mcp_workflow_tools.py:7
# Component id: og.source.a3_og_features.test_map_terrain_sees_extended_mcp_workflow_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_sees_extended_mcp_workflow_tools(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Store and query context through MCP.",
        required_capabilities={
            "tools": ["phase0_recon", "context_memory_store", "context_memory_query", "map_terrain"],
        },
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["tools"]["phase0_recon"] == "exists"
    assert result.inventory_check["tools"]["context_memory_store"] == "exists"
