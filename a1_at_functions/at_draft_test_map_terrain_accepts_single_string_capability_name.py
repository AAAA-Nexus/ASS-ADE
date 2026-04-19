# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_map_terrain_accepts_single_string_capability_name.py:5
# Component id: at.source.ass_ade.test_map_terrain_accepts_single_string_capability_name
__version__ = "0.1.0"

def test_map_terrain_accepts_single_string_capability_name(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Read one file.",
        required_capabilities={"tools": "read_file"},
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["tools"]["read_file"] == "exists"
