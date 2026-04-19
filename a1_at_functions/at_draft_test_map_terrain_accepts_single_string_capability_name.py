# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_map_terrain_accepts_single_string_capability_name.py:7
# Component id: at.source.a1_at_functions.test_map_terrain_accepts_single_string_capability_name
from __future__ import annotations

__version__ = "0.1.0"

def test_map_terrain_accepts_single_string_capability_name(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Read one file.",
        required_capabilities={"tools": "read_file"},
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["tools"]["read_file"] == "exists"
