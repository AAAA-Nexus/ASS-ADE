# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_map_terrain_proceed_for_existing_local_and_hosted_tool.py:7
# Component id: at.source.a1_at_functions.test_map_terrain_proceed_for_existing_local_and_hosted_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_proceed_for_existing_local_and_hosted_tool(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Read a file and authorize the action.",
        required_capabilities={
            "tools": ["read_file", "authorize_action"],
            "harnesses": ["pytest"],
        },
        working_dir=tmp_path,
        hosted_tools=["authorize_action"],
    )

    assert result.verdict == "PROCEED"
    assert result.missing_capabilities == []
    assert result.inventory_check["tools"]["read_file"] == "exists"
    assert result.inventory_check["tools"]["authorize_action"] == "exists"
